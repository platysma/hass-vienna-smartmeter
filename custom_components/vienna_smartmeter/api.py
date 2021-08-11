"""Vienna Smartmeter API Client."""
import asyncio
import logging
import socket
from datetime import datetime
from urllib import parse

import aiohttp
import async_timeout
from lxml import html

from .errors import SmartmeterLoginError

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ViennaSmartmeterApiClient:

    API_URL = "https://service.wienernetze.at/rest/smp/1.0/"
    API_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    AUTH_URL = "https://service.wienerstadtwerke.at/auth/realms/wienernetze/protocol/openid-connect/"  # noqa

    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Initialize Smartmeter client."""
        self._username = username
        self._password = password
        self._session = session
        self.access_token = None

    async def _get_login_action(self) -> str:
        args = {
            "client_id": "client-smp-public",
            "redirect_uri": "https://www.wienernetze.at/wnapp/smapp/",
            "response_mode": "fragment",
            "response_type": "code",
            "scope": "openid",
            "nonce": "",
            "prompt": "login",
        }
        login_url = self.AUTH_URL + "auth?" + parse.urlencode(args)

        async with self._session.request("GET", login_url) as resp:
            tree = html.fromstring(resp.content)
            return tree.xpath("(//form/@action)")[0]

    async def _get_auth_code(self) -> str:

        action = await self._get_login_action()

        async with self._session.request(
            "POST",
            action,
            data={"username": self._username, "password": self._password},
            allow_redirects=False,
        ) as resp:
            if "Location" not in resp.headers:
                raise SmartmeterLoginError(
                    "Authentication failed. Check user credentials."
                )
            auth_code = resp.headers["Location"].split("&code=", 1)[1]
            return auth_code

    async def _refresh_token(self) -> str:
        """Return a valid access token."""
        async with self._session.request(
            "POST",
            self.AUTH_URL + "token",
            data={
                "code": await self._get_auth_code(),
                "grant_type": "authorization_code",
                "client_id": "client-smp-public",
                "redirect_uri": "https://www.wienernetze.at/wnapp/smapp/",
            },
        ) as resp:
            if resp.status_code != 200:
                raise SmartmeterLoginError(
                    "Authentication failed. Check user credentials."
                )

            self.access_token = await resp.json()["access_token"]

        _LOGGER.debug("Successfully authenticated Smart Meter API")

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        pass

    def _dt_string(self, datetime_string):
        return datetime_string.strftime(self.API_DATE_FORMAT)[:-3] + "Z"

    def _get_first_zaehlpunkt(self) -> str:
        """Get first zaehlpunkt."""
        return self.get_zaehlpunkte()[0]["zaehlpunkte"][0]["zaehlpunktnummer"]

    async def get_zaehlpunkte(self) -> list:
        """Get zaehlpunkte for currently logged in user."""
        return await self._request("m/zaehlpunkte")

    async def get_verbrauch_raw(
        self, date_from: datetime, date_to=datetime.now(), zaehlpunkt=None
    ) -> dict:
        """Get verbrauch_raw from the API."""
        if zaehlpunkt is None:
            zaehlpunkt = self._get_first_zaehlpunkt()
        endpoint = "m/messdaten/zaehlpunkt/{}/verbrauchRaw".format(zaehlpunkt)
        query = {
            "dateFrom": self._dt_string(date_from),
            "dateTo": self._dt_string(date_to),
            "granularity": "DAY",
        }
        return await self._request(endpoint, query=query)

    async def async_get_profil(self) -> dict:
        """Get profil of logged in user."""
        return await self._request("w/user/profile")

    async def _request(
        self, endpoint: str, base_url=None, method="GET", data=None, query=None
    ) -> dict:
        """Send requests to the Smartmeter API"""

        if base_url is None:
            base_url = self.API_URL
        url = "{0}{1}".format(base_url, endpoint)

        if query:
            separator = "?" if "?" not in endpoint else "&"
            url += separator + parse.urlencode(query)

        _LOGGER.debug(f"REQUEST: {url}")

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.request(
                    method, url, headers=headers, json=data
                )
                _LOGGER.debug(f"REQUEST: {response}")
                if response.status == 401:
                    await self._refresh_token()
                    return await self._request(endpoint, base_url, method, data, query)
                return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                f"Timeout error fetching information from {url} - {exception}"
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(f"Error parsing information from {url} - {exception}")
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(f"Error fetching information from {url} - {exception}")
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error(f"Something really wrong happened! - {exception}")

[![GitHub Workflow Status][workflow-shield]][workflow]
[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]
[![hacs][hacsbadge]][hacs]
[![GitHub Activity][commits-shield]][commits]

<p align="center">
  <a href="https://github.com/leikoilja/ha-google-home">
    <img src="https://blog.wienernetze.at/wp-content/uploads/2020/10/WN-LOGO-Plus-Der-Wiener-Netze-Blog_2x.png" alt="Logo" height="150">
  </a>
</p>

<h3 align="center">Vienna Smart Meter Home Assistant Integration</h3>

<p align="center">
  This custom integration aims to provide meter readings from Vienna Smart Meter in your Home Assistant instance.
</p>

<p align="center">
  :collision: <b>Breaking Changes:</b>
  This Home Assistant Integration is still in the initial development phase, and may introduce breaking changes at any time.
</p>

## Sensors

The component will set up a `sensor` platform which displays the latest meter reading available from the [unofficial Smart Meter API][smart-meter]. At this time, only a single smart meter (the one specified as the main meter) can be tracked.

## Getting Started

### Prerequisites

Home Assistant v2021.8.0 or above.

### HACS Installation

Currently a HACS installation is not available.

<!-- You can find it in the default HACS repo. Just search for `Vienna Smart Meter`. -->

### Manual Installation

1. Download the [latest release](releases/latest/download/release.zip) zip file.
2. Unpack it.
3. Copy the `vienna_smartmeter` directory from the unpacked archive to `custom_components` in your Home Assistant configuration directory (If you do not have a `custom_components` directory there, you need to create it.).
4. Restart Home Assistant
5. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Vienna Smart Meter"

## Contribution

If you encounter issues or have any suggestions consider opening issues and contributing through PR. If you want to contribute please read the [Contribution guidelines](CONTRIBUTING.md).

[workflow-shield]: https://img.shields.io/github/workflow/status/platysma/hass-vienna-smartmeter/Linting?style=for-the-badge
[workflow]: https://github.com/platysma/hass-vienna-smartmeter/actions
[releases-shield]: https://img.shields.io/github/release/platysma/hass-vienna-smartmeter.svg?style=for-the-badge
[releases]: https://github.com/platysma/hass-vienna-smartmeter/releases
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/platysma/hass-vienna-smartmeter.svg?style=for-the-badge
[commits]: https://github.com/platysma/hass-vienna-smartmeter/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/platysma/hass-vienna-smartmeter.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[smart-meter]: https://github.com/platysma/vienna-smartmeter

[![Python package](https://github.com/rpliva/hacs-evmate/actions/workflows/pythonpackage.yaml/badge.svg?branch=main)](https://github.com/rpliva/hacs-evmate/actions/workflows/pythonpackage.yaml)
[![Validate with hassfest](https://github.com/rpliva/hacs-evmate/actions/workflows/hassfest.yaml/badge.svg?branch=main)](https://github.com/rpliva/hacs-evmate/actions/workflows/hassfest.yaml)
[![HACS Action](https://github.com/rpliva/hacs-evmate/actions/workflows/validate.yaml/badge.svg?branch=main)](https://github.com/rpliva/hacs-evmate/actions/workflows/validate.yaml)
[![Latest Commit](https://badgen.net/github/last-commit/rpliva/hacs-evmate/main)](https://github.com/rpliva/hacs-evmate/commit/HEAD)

EVMate IoTMeter Integration for Home Assistant
==============================================

This is an integration for Home Assistant that allows you to monitor your EVMate IoTMeter device. This integration fetches the latest data and displays it as a sensor in Home Assistant. 


Installation
------------

### HACS (Home Assistant Community Store)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jmdevita&repository=parcel-ha&category=Integration)

### Other ways to Install

1.  Ensure that you have HACS installed in your Home Assistant instance.
2.  Add this repository to HACS as a custom repository.
3.  Search for "EVMate" in HACS and install it.

Configuration
-------------

### Adding the Integration

1.  In Home Assistant, navigate to **Configuration** > **Devices & Services**.
2.  Click on **Add Integration** and search for "EVMate".
3.  Follow the prompts to enter IP address of yout IoTMeter device and port (default value is 8000).

### Configuration Options

You can configure the integration options by navigating to **Configuration** > **Devices & Services**, selecting the EVMate integration, and clicking on **Options**.


Development
-----------

### Prerequisites

-   Home Assistant
-   HACS

Contributing
------------

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/rpliva/hacs-evmate/pulls).

License
-------

This project is licensed under the  MIT license. See the [LICENSE](/LICENSE) file for details.

Support
-------

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/rpliva/hacs-evmate/issues).


* * * * *

**Note:** This integration is unofficial and not affiliated with the EVMate developers.
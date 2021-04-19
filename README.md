# unfilter
A simple app python app that will change the DNS settings of a Windows PC to disable DNS based filtering. This is intended for libraries that are using eRate and want to allow patrons to disable their own filtering.

## Setup
* Rename config.ini.example to config.ini
* Rename ils.ini.example to ils.ini
* Edit files with needed information

## Usage Requirements
* Currently only works with the Sirsi Sympnony ILS that has web services enabled. It should work with Horizon, but has never been tested.
* Use SafeDNS, 1.1.1.3, Pi-Hole with the pi_blocklist_porn_all.list, or some other DNS based filtering system to filter adult content. 
* Use PyInstaller to create an EXE of this program, and install on the computers you want to allow the filter to be removed. 
* The profile/user account will need to be added to the "Network Configuration Operators" security group.

## Still working on: 
- Fixing the menu setup via the config.ini
- Add the option for a logging server to track date, time, card number, and PC name when filtering is disabled
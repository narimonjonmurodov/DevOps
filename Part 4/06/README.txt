GoAccess Monitoring Script

Description:
This script launches the GoAccess web interface to analyze nginx log files
generated in Part 4.

Requirements:

* Ubuntu 20.04 or compatible Linux system
* GoAccess installed
* Nginx logs located in ../04 directory from Task 4

Installation:
If GoAccess is not installed, install it using:

sudo apt update
sudo apt install goaccess

usage:
./main.sh <OPTIONS>

OPTIONS:
  1 - Analyze logs in terminal (GoAccess)
  2 - Start GoAccess web interface
  
Features:
The dashboard provides information about:

* Request statistics
* Unique visitors (IP addresses)
* HTTP status codes
* Error requests
* Requested URLs
* Browsers and operating systems

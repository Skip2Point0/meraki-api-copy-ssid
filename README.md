# meraki-api-copy-ssid

Summary:

Purpose of this script is to copy SSID settings from one wireless network to another. Multiple SSIDs and multiple destination 
networks are supported. By default: copies SSID > Access Control, Splash Page, Firewall L3, and Traffic Shaping settings.

Requirements:

1) Interpreter: Python 3.8.0+
2) Python Packages: requests, json
3) Networks where SSID will be copied to must have at least one AP, or were setup as a Wireless
   Network when were first created.
4) API support for the Organization is enabled in Meraki Dashboard. Admin has generated custom API key.

How to run:

1) Open cp_ssid_settings.py with your favorite text editor and edit PARAMETERS sections of the script. 
2) To turn off settings that you do not want to copy:
   1) To disable copy of Splash Page settings comment out Line 249.
   2) To disable copy of Firewall L3 rules comment out line 250.
   3) To disable copy of Traffic Shaping settings comment out line 251.
2) Run python3 cp_ssid_settings.py in the terminal.
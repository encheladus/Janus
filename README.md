# Spoof Tool
***
## Project's Goal
A Python tool that allows users to:
- Temporarily spoof the MAC address of a selected network interface
- Modify the User-Agent for HTTP requests
- Confirm that the spoofing actions were successful
***
## Disclaimer
- Some commands may require root access
- This tool is not intended for illegal use
- All operations are documented — please read the instructions
***
## Technical Stack
- Python 3.12
- Possible libraries (to be confirmed):
    - `subprocess` — for executing system commands (MAC spoofing)
    - `re` — for parsing command outputs
    - `requests` — for making HTTP requests with a custom User-Agent
    - `argparse` — for command-line interaction
    - `fake-useragent` — for generating random User-Agents
    - `pytest` — for unit testing
***
## Tree files
.
└── spoof_tool/
    ├── spoof_mac.py
    ├── spoof_useragent.py
    ├── main.py
    ├── tests/
    │   └── test_spoof_mac.py
    │   └── test_spoof_useragent.py
    └── README.md
***
## Main functions 
### `spoof_mac.py`
- `get_current_mac(interface)` — returns the current MAC address
- `change_mac(interface, new_mac)` — changes the MAC address
- `generate_random_mac()` — generates a random MAC address
### `spoof_useragent.py`
- `get_random_useragent()` — returns a random User-Agent
- `make_request_with_useragent(url, user_agent)` — makes an HTTP request with the spoofed User-Agent
### `main.py`
- CLI interface to choose and launch the spoofing actions
## Expected result
- The MAC address change
- The user agent change
- You have a confirmation of the changes
***
## What can this tool help you with?
| Case                           | Spoof MAC | Spoof UA | Useful to see the site ? |
|--------------------------------|-----------|----------|--------------------------|
| Bypass WAF filtering           | N         | Y        | N                        |
| Silent scan                    | Y         | Y        | N                        |
| Turning hidden on WiFi network | Y         | N        | N                        |
| Analyse mobile version         | N         | Y        | Sometimes Yes            |
***
## Which tools can you combine with this spoof tool?
 Tools         | Spoof MAC useful ? | Spoof UA useful ? |
|---------------|--------------------|-------------------|
| nmap          | Y                  | N                 |
| dirp/gobuster | N                  | Y                 |
| nikto         | N                  | Y                 |
| Burp Suite    | N                  | Y                 |
| wireshark     | Y                  | N                 |
***
This project was made for fun and learning purposes :) 
"""
spoof_mac.py

This module handles MAC address operations:
- Retrieve current MAC address
- Generate random MAC address
- Change MAC address using system commands

Author: TonNom
Created: 2025-05-27
"""

import subprocess
import re
import random


def get_current_mac(operating_system = "Unix", interface = "wlan0"):
    """
    Get the current MAC address of a given network interface.

    Args:
        operating_system (str): the name of the operating system you are using (e.g., "Unix")
        interface (str): The name of the network interface (e.g., "en0").

    Returns:
        str: MAC address as "XX:XX:XX:XX:XX:XX" or None if not found.
    """
    mac_filter = r'ether\s+([0-9a-f:]{2}(?::[0-9a-f:]{2}){5})' #I tried my best, but I hate this so much, chatGPT helped me to build for the regex pattern
    win_mac_filter = r'Physical Address[.\s]*: ([0-9A-Fa-f\-]{17})'
    os = operating_system.lower()

    if os == "windows":
        try:
            output = subprocess.check_output(['ipconfig']).decode(errors='ignore')
            interface_blocks = output.split("\r\n\r\n")
            for block in interface_blocks:
                if interface in block:
                    match = re.search(win_mac_filter, block)
                    if match:
                        return match.group(1)

        except Exception as e:
            print("something occurred, please check", e)
            return
    elif os in ["unix", "macos"]:
        try:
            output = subprocess.check_output(['ifconfig', interface]).decode(errors='ignore')
            my_mac_addresses = re.search(mac_filter, output)
            return my_mac_addresses.group(1)
        except Exception as e:
            print("something occurred, please check", e)
            return
    else:
        print("Enter a carried OS : 1.Windows, 2.Unix, 3.MacOS")
        return

def change_mac(interface, new_mac):
    pass

def generate_random_mac(operating_system = "unix"): #I found this code https://codingfleet.com/transformation-details/generating-a-random-mac-address-in-python/
    """
    Generate a random MAC address formatted according to the given operating system.

    Parameters:
        operating_system (str): The target OS for which the MAC address should be generated.
                                Accepted values are "unix", "macos", or "windows" (case-insensitive).
                                Defaults to "unix".

    Returns:
        str or None: A string representing the new MAC address in the appropriate format:
                     - Colon-separated (e.g., 'a2:bc:de:f1:23:45') for Unix/macOS
                     - Hyphen-separated (e.g., 'A2-BC-DE-F1-23-45') for Windows
                     Returns None if the OS is not recognized, and prints a warning message.

    Notes:
        - The second digit is guaranteed to be an even hexadecimal character to ensure
          the generated MAC is unicast and locally administered.
        - This function uses random selection and is non-deterministic.
        - The initial version of this function is based on an example from:
          https://codingfleet.com/transformation-details/generating-a-random-mac-address-in-python/
    """
    os = operating_system.lower()

    if os in ["unix", "macos"]:
        digits = [random.choice('0123456789abcdef') for _ in range(11)]
        second_digit = random.choice('02468ace')
        digits.insert(1, second_digit)
        new_mac_address = ':'.join(''.join(digits[i:i + 2]) for i in range(0, 12, 2))
        return new_mac_address


    elif os == "windows":
        digits = [random.choice('0123456789ABCDEF') for _ in range(11)]
        second_digit = random.choice('02468ACE')
        digits.insert(1, second_digit)
        new_mac_address = '-'.join(''.join(digits[i:i + 2]) for i in range(0, 12, 2))
        return new_mac_address

    else:
        print("Enter a carried OS : 1.Windows, 2.Unix, 3.MacOS")
        return

if __name__ == '__main__':
    mac_address = get_current_mac("unix", "eth0")
    print(mac_address)
    print(generate_random_mac("unix"))
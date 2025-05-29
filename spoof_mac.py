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
try:
    import winreg
except ImportError:
    winreg = None



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

def change_mac(operating_system = 'unix', interface = 'eth0'):
    """
    Changes the MAC address of a network interface based on the operating system.

    This function generates a random MAC address and applies it to the specified
    network interface. It supports Unix/Linux, macOS, and Windows platforms, using
    OS-specific tools and methods.

    Parameters
    ----------
    operating_system : str, optional
        The operating system of the host machine. Supported values are
        'unix', 'macos', or 'windows'. Default is 'unix'.
    interface : str, optional
        The name of the network interface to modify (e.g., 'eth0', 'Wi-Fi').
        Default is 'eth0'.

    Returns
    -------
    None
        The function prints the status and results of each step but does not return a value.

    Raises
    ------
    None
        Exceptions are caught and printed; the function does not raise errors directly.

    Notes
    -----
    - For Unix/Linux: uses `ifconfig` and `macchanger`.
    - For macOS: uses `ifconfig` to manually set the MAC address.
    - For Windows: modifies the registry via `winreg` and restarts the interface using `netsh`.
    - Administrator/root privileges are required for all platforms.
    - Regarding windows winreg use, I was able to find a detailed code existing explaining how to find the register
    """
    os = operating_system.lower()
    new_mac = generate_random_mac(os)
    if os == "unix":
        try:
            print(f'current MAC Address: {get_current_mac(os, interface)} \n Turn off eth0' )
            subprocess.check_output(['ifconfig', interface, 'down']).decode(errors='ignore')
            print('Success \n Start macchange')
            subprocess.check_output(['macchanger', '-m', new_mac, interface]).decode(errors='ignore')
            print('Success macchange \n Turn on eth0')
            subprocess.check_output(['ifconfig', interface, 'up']).decode(errors='ignore')
            return print(f'Success. new MAC Address: {get_current_mac('unix', 'eth0')}')
        except Exception as e:
            print("something occurred, please check", e)
            return
    elif os == 'macos':
        try:
            print(f'current MAC Address: {get_current_mac(os, interface)} \n Turn off eth0')
            subprocess.check_output(['ifconfig', interface, 'down']).decode(errors='ignore')
            print('Success \n Start macchange')
            subprocess.check_output(['ifconfig', interface, 'ether',new_mac]).decode(errors='ignore')
            print('Success macchange \n Turn on eth0')
            subprocess.check_output(['ifconfig', interface, 'up']).decode(errors='ignore')
            return print(f'Success. new MAC Address: {get_current_mac('unix', 'eth0')}')
        except Exception as e:
            print("something occurred, please check", e)
            return
    elif os == 'windows':
        if winreg is None:
            print("winreg module is not available on this platform.")
            return
        try:
            print(f'Current MAC: {get_current_mac(os, interface)}')

            reg_path = r'SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}'
            found = False
            with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hklm:
                with winreg.OpenKey(hklm, reg_path) as base_key:
                    for i in range(1000):
                        try:
                            subkey_name = f"{i:04}"
                            with winreg.OpenKey(base_key, subkey_name, 0, winreg.KEY_ALL_ACCESS) as subkey:
                                try:
                                    reg_mac = winreg.QueryValueEx(subkey, "NetCfgInstanceId")[0]
                                    reg_desc = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                                    if interface.lower() in reg_desc.lower():
                                        winreg.SetValueEx(subkey, "NetworkAddress", 0, winreg.REG_SZ,
                                                          new_mac.replace(":", ""))
                                        found = True
                                        print(f"MAC changed in the register : {new_mac.replace('-', '')}")
                                        break
                                except FileNotFoundError:
                                    continue
                        except OSError:
                            break
            if not found:
                print("Cannot found the interface in the register.")
                return

            subprocess.check_call(['netsh', 'interface', 'set', 'interface', interface, 'admin=disable'])
            subprocess.check_call(['netsh', 'interface', 'set', 'interface', interface, 'admin=enable'])
            print(f"Success macchange {interface}.")

        except Exception as e:
            print("something occurred, please check", e)
            return
    else:
        print("Enter a carried OS : 1.Windows, 2.Unix, 3.MacOS or an existing interface")

if __name__ == '__main__':
    new_mac = generate_random_mac('windows')
    change_mac('unix', 'eth0')
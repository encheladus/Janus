from unittest.mock import patch
from ..spoof_mac import get_current_mac, generate_random_mac

"""
Unit tests for the `spoof_mac` module.

This test suite verifies the behavior of two main functions:
- `get_current_mac`: retrieves the current MAC address of a network interface depending on the operating system.
- `generate_random_mac`: generates a new random MAC address in a format appropriate for the specified OS.

The tests cover:
- Successful MAC address extraction for Unix, macOS, and Windows.
- Handling cases where no MAC address is found.
- Proper handling of exceptions (e.g., command failures).
- Random MAC address generation for each OS format.
- Validation of behavior when an invalid OS is specified.

Mocking is used to simulate system command outputs and random choices.
"""

def test_get_current_mac_unix_success():
    """Test retrieving the MAC address on Unix with valid output."""
    fake_output = "wlan0: flags=... \n    ether ab:cd:ef:12:34:56"
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = fake_output.encode()
        result = get_current_mac("unix", "wlan0")
        assert result == "ab:cd:ef:12:34:56"

def test_get_current_mac_macos_success():
    """Test retrieving the MAC address on macOS with valid output."""
    fake_output = "en0: flags=... \n    ether ab:cd:ef:12:34:56"
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = fake_output.encode()
        result = get_current_mac("macos", "en0")
        assert result == "ab:cd:ef:12:34:56"

def test_get_current_mac_windows_success():
    """Test retrieving the MAC address on Windows with valid output."""
    fake_output = """
    Windows IP Configuration

       Host Name . . . . . . . . . . . . : MY-COMPUTER
       Primary Dns Suffix  . . . . . . . : 
       Node Type . . . . . . . . . . . . : Hybrid
       IP Routing Enabled. . . . . . . . : No
       WINS Proxy Enabled. . . . . . . . : No

    Ethernet adapter Ethernet:

       Connection-specific DNS Suffix  . : localdomain
       Description . . . . . . . . . . . : Intel(R) Ethernet Connection
       Physical Address. . . . . . . . . : AB-CD-EF-12-34-56
       DHCP Enabled. . . . . . . . . . . : Yes
       Autoconfiguration Enabled . . . . : Yes
       IPv4 Address. . . . . . . . . . . : 192.168.1.10
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . : 192.168.1.1
    """
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = fake_output.encode()
        result = get_current_mac("windows", "Ethernet")
        assert result == "AB-CD-EF-12-34-56"

def test_get_current_mac_unix_no_match():
    """Test handling the case where no MAC address is found on Unix."""
    fake_output = "wlan0: flags=... \n"
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = fake_output.encode()
        result = get_current_mac("unix", "wlan0")
        assert result is None

def test_get_current_mac_macos_no_match():
    """Test handling the case where no MAC address is found on macOS."""
    fake_output = "en0: flags=... \n"
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = fake_output.encode()
        result = get_current_mac("macos", "en0")
        assert result is None

def test_get_current_mac_windows_no_match():
    """Test handling the case where no MAC address is found on Windows."""
    fake_output = """
    Windows IP Configuration

       Host Name . . . . . . . . . . . . : MY-COMPUTER
       Primary Dns Suffix  . . . . . . . : 
       Node Type . . . . . . . . . . . . : Hybrid
       IP Routing Enabled. . . . . . . . : No
       WINS Proxy Enabled. . . . . . . . : No
    """
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = fake_output.encode()
        result = get_current_mac("windows", "Ethernet")
        assert result is None

def test_get_current_mac_unix_error():
    """Test error handling when an exception is raised on Unix."""
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.side_effect = Exception("Boom")  # Simule une erreur
        result = get_current_mac("unix", "wlan0")
        assert result is None

def test_get_current_mac_macos_error():
    """Test error handling when an exception is raised on macOS."""
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.side_effect = Exception("Boom")  # Simule une erreur
        result = get_current_mac("macos", "en0")
        assert result is None

def test_get_current_mac_windows_error():
    """Test error handling when an exception is raised on Windows."""
    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.side_effect = Exception("Boom")  # Simule une erreur
        result = get_current_mac("windows", "Ethernet")
        assert result is None

def test_generate_random_mac_unix_success():
    """Test generating a random MAC address in Unix format."""
    initial_digits = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5']  # 11 chars
    second_digit = '2'
    side_effects = initial_digits + [second_digit]
    with patch('random.choice') as mock_choice:
        mock_choice.side_effect = side_effects
        mac = generate_random_mac('unix')
        assert mac == 'a2:bc:de:f1:23:45'

def test_generate_random_mac_macos_success():
    """Test generating a random MAC address in macOS format."""
    initial_digits = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5']  # 11 chars
    second_digit = '2'
    fake_output = initial_digits + [second_digit]
    with patch('random.choice') as mock_choice:
        mock_choice.side_effect = fake_output
        mac = generate_random_mac('macos')
        assert mac == 'a2:bc:de:f1:23:45'

def test_generate_random_mac_windows_success():
    """Test generating a random MAC address in Windows format."""
    initial_digits = ['A', 'B', 'C', 'D', 'E', 'F', '1', '2', '3', '4', '5']  # 11 chars
    second_digit = '2'
    fake_output = initial_digits + [second_digit]
    with patch('random.choice') as mock_choice:
        mock_choice.side_effect = fake_output
        mac = generate_random_mac('windows')
        assert mac == 'A2-BC-DE-F1-23-45'


def test_generate_random_mac_invalid_os(capsys):
    """Test behavior when an unsupported OS is provided: checks printed message and return value."""
    mac = generate_random_mac('invalid_os')
    captured = capsys.readouterr()
    assert "Enter a carried OS : 1.Windows, 2.Unix, 3.MacOS" in captured.out
    assert mac is None

def test_change_mac_unix_success():
    pass
def test_change_mac_macos_success():
    pass
def test_change_mac_windows_success():
    pass
def test_change_mac_unix_error():
    pass
def test_change_mac_macos_error():
    pass
def test_change_mac_windows_error():
    pass
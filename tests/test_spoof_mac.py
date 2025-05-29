from unittest.mock import patch, MagicMock
from ..spoof_mac import get_current_mac, generate_random_mac, change_mac
import sys
import pytest
import subprocess

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
- Successfully change the MAC address to a fake one

Mocking is used to simulate system command outputs and random choices.
Pytest allow us to skip the test for windows if it's tested on a device other than windows
"""


# ----------------------
# Tests for get_current_mac
# ----------------------

@patch("subprocess.check_output")
def test_get_current_mac_unix_success(mock_check_output):
    """Test retrieving the MAC address on Unix with valid output."""
    fake_output = "wlan0: flags=... \n    ether ab:cd:ef:12:34:56"
    mock_check_output.return_value = fake_output.encode()
    result = get_current_mac("unix", "wlan0")
    assert result == "ab:cd:ef:12:34:56"

@patch("subprocess.check_output")
def test_get_current_mac_macos_success(mock_check_output):
    """Test retrieving the MAC address on macOS with valid output."""
    fake_output = "en0: flags=... \n    ether ab:cd:ef:12:34:56"
    mock_check_output.return_value = fake_output.encode()
    result = get_current_mac("macos", "en0")
    assert result == "ab:cd:ef:12:34:56"

@patch("subprocess.check_output")
def test_get_current_mac_windows_success(mock_check_output):
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
    mock_check_output.return_value = fake_output.encode()
    result = get_current_mac("windows", "Ethernet")
    assert result == "AB-CD-EF-12-34-56"

@patch("subprocess.check_output")
def test_get_current_mac_unix_no_match(mock_check_output):
    """Test handling the case where no MAC address is found on Unix."""
    fake_output = "wlan0: flags=... \n"
    mock_check_output.return_value = fake_output.encode()
    result = get_current_mac("unix", "wlan0")
    assert result is None

@patch("subprocess.check_output")
def test_get_current_mac_macos_no_match(mock_check_output):
    """Test handling the case where no MAC address is found on macOS."""
    fake_output = "en0: flags=... \n"
    mock_check_output.return_value = fake_output.encode()
    result = get_current_mac("macos", "en0")
    assert result is None

@patch("subprocess.check_output")
def test_get_current_mac_windows_no_match(mock_check_output):
    """Test handling the case where no MAC address is found on Windows."""
    fake_output = """
    Windows IP Configuration

       Host Name . . . . . . . . . . . . : MY-COMPUTER
       Primary Dns Suffix  . . . . . . . : 
       Node Type . . . . . . . . . . . . : Hybrid
       IP Routing Enabled. . . . . . . . : No
       WINS Proxy Enabled. . . . . . . . : No
    """
    mock_check_output.return_value = fake_output.encode()
    result = get_current_mac("windows", "Ethernet")
    assert result is None

@patch("subprocess.check_output")
def test_get_current_mac_unix_error(mock_check_output):
    """Test error handling when an exception is raised on Unix."""
    mock_check_output.side_effect = Exception("Boom")  # Simule une erreur
    result = get_current_mac("unix", "wlan0")
    assert result is None

@patch("subprocess.check_output")
def test_get_current_mac_macos_error(mock_check_output):
    """Test error handling when an exception is raised on macOS."""
    mock_check_output.side_effect = Exception("Boom")  # Simule une erreur
    result = get_current_mac("macos", "en0")
    assert result is None

@patch("subprocess.check_output")
def test_get_current_mac_windows_error(mock_check_output):
    """Test error handling when an exception is raised on Windows."""
    mock_check_output.side_effect = Exception("Boom")  # Simule une erreur
    result = get_current_mac("windows", "Ethernet")
    assert result is None


# ----------------------
# Tests for generate_random_mac
# ----------------------

@patch("random.choice")
def test_generate_random_mac_unix_success(mock_choice):
    """Test generating a random MAC address in Unix format."""
    initial_digits = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5']  # 11 chars
    second_digit = '2'
    side_effects = initial_digits + [second_digit]
    mock_choice.side_effect = side_effects
    mac = generate_random_mac('unix')
    assert mac == 'a2:bc:de:f1:23:45'
@patch("random.choice")
def test_generate_random_mac_macos_success(mock_choice):
    """Test generating a random MAC address in macOS format."""
    initial_digits = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5']  # 11 chars
    second_digit = '2'
    fake_output = initial_digits + [second_digit]
    mock_choice.side_effect = fake_output
    mac = generate_random_mac('macos')
    assert mac == 'a2:bc:de:f1:23:45'
@patch("random.choice")
def test_generate_random_mac_windows_success(mock_choice):
    """Test generating a random MAC address in Windows format."""
    initial_digits = ['A', 'B', 'C', 'D', 'E', 'F', '1', '2', '3', '4', '5']  # 11 chars
    second_digit = '2'
    fake_output = initial_digits + [second_digit]
    mock_choice.side_effect = fake_output
    mac = generate_random_mac('windows')
    assert mac == 'A2-BC-DE-F1-23-45'


def test_generate_random_mac_invalid_os(capsys):
    """Test behavior when an unsupported OS is provided: checks printed message and return value."""
    mac = generate_random_mac('invalid_os')
    captured = capsys.readouterr()
    assert "Enter a carried OS : 1.Windows, 2.Unix, 3.MacOS" in captured.out
    assert mac is None


# ----------------------
# Tests for change_mac
# ----------------------


@patch('spoof_mac.get_current_mac', return_value="aa:bb:cc:dd:ee:ff")
@patch('spoof_mac.generate_random_mac', return_value="02:00:00:00:00:01")
@patch('spoof_mac.subprocess.check_output', return_value=b"")
def test_change_mac_unix_success(mock_subprocess, mock_gen_mac, mock_get_mac, capsys):
    """Test a successful Mac address update on unix os"""
    change_mac('unix', 'eth0')
    output = capsys.readouterr().out
    assert "Success" in output
    assert mock_subprocess.call_count == 5

@patch('spoof_mac.get_current_mac', return_value="aa:bb:cc:dd:ee:ff")
@patch('spoof_mac.generate_random_mac', return_value="02:00:00:00:00:01")
@patch('spoof_mac.subprocess.check_output', return_value=b"")
def test_change_mac_macos_success(mock_subprocess, mock_gen_mac, mock_get_mac, capsys):
    """Test a successful Mac address update on mac os"""
    change_mac('macos', 'en0')
    output = capsys.readouterr().out
    assert "Success" in output
    assert mock_subprocess.call_count == 5

@pytest.mark.skipif(sys.platform != "win32", reason="winreg only available on Windows")
@patch('spoof_mac.get_current_mac', return_value="AA-BB-CC-DD-EE-FF")
@patch('spoof_mac.generate_random_mac', return_value="A2-BC-DE-F1-23-45")
@patch('spoof_mac.winreg')
@patch('spoof_mac.subprocess.check_call')
def test_change_mac_windows_success(mock_subprocess, mock_winreg, mock_gen_mac, mock_get_mac, capsys):
    """Test a successful Mac address update on windows os"""
    mock_reg = MagicMock()
    mock_key = MagicMock()
    mock_subkey = MagicMock()

    mock_winreg.ConnectRegistry.return_value.__enter__.return_value = mock_reg
    mock_winreg.OpenKey.side_effect = [mock_key, mock_subkey]
    mock_winreg.QueryValueEx.side_effect = [
        ("some-instance-id",), ("Ethernet",)
    ]

    change_mac('windows', 'Ethernet')
    output = capsys.readouterr().out
    assert "MAC changed in the register" in output
    assert "Success macchange" in output
    assert mock_subprocess.call_count == 2

@patch('spoof_mac.subprocess.check_output')
def test_change_mac_unix_error(mock_check_output, capsys):
    """Test an error while Mac address update on unix os"""
    mock_check_output.side_effect = subprocess.CalledProcessError(returncode=1, cmd='ifconfig')
    change_mac('unix', 'eth0')
    output = capsys.readouterr().out
    assert "something occurred, please check" in output

@patch('spoof_mac.subprocess.check_output')
def test_change_mac_macos_error(mock_check_output, capsys):
    """Test an error while Mac address update on mac os"""
    mock_check_output.side_effect = subprocess.CalledProcessError(returncode=1, cmd='ifconfig')
    change_mac('macos', 'en0')
    output = capsys.readouterr().out
    assert "something occurred, please check" in output

@pytest.mark.skipif(sys.platform != "win32", reason="winreg only available on Windows")
@patch('spoof_mac.get_current_mac', return_value="AA-BB-CC-DD-EE-FF")
@patch('spoof_mac.generate_random_mac', return_value="A2-BC-DE-F1-23-45")
@patch('spoof_mac.winreg')
@patch('spoof_mac.subprocess.check_call')
def test_change_mac_windows_error(mock_subprocess, mock_winreg, mock_gen_mac, mock_get_mac, capsys):
    """Test an error while Mac address update on windows os"""
    mock_reg = MagicMock()
    mock_key = MagicMock()
    mock_subkey = MagicMock()
    mock_winreg.ConnectRegistry.return_value.__enter__.return_value = mock_reg
    mock_winreg.OpenKey.side_effect = [mock_key, mock_subkey]
    mock_winreg.QueryValueEx.side_effect = Exception("Registry error")
    change_mac('windows', 'Ethernet')
    output = capsys.readouterr().out
    assert "something occurred, please check" in output
def test_change_mac_invalid_args(capfd):
    """Test behavior when an unsupported OS is provided: checks printed message and return value."""
    change_mac("beos", "eth0")
    output, err = capfd.readouterr()
    assert "Enter a carried OS" in output
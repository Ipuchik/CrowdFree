import subprocess
import re
import platform


def ping_device(ip):
    # Determine the command based on the operating system
    if platform.system().lower() == "windows":
        # Windows ping command
        result = subprocess.run(['ping', ip, '-n', '1'], capture_output=True, text=True)
    else:
        # Linux and macOS ping command
        result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True)
   
    return result.returncode == 0  # Returns True if the device is reachable


def count_live_wifi_devices():
    # Execute the arp command to get the list of devices
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)


    # Split the output into lines
    lines = result.stdout.splitlines()


    # Initialize a count for devices
    live_device_count = 0
   
    print("Currently connected Wi-Fi devices:")
   
    for line in lines:
        # Use regex to find valid IP addresses
        ip_match = re.search(r'(\d{1,3}\.){3}\d{1,3}', line)
        if ip_match:
            ip = ip_match.group()
            # Check if the device is live
            if ping_device(ip):
                print(f"Live Device IP: {ip}")
                live_device_count += 1
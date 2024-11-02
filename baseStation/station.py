import nmap

NUM_STATIONS = 1
STATION_NAME = "SBBLT2_1"

class Station:
    def __init__(self, name) -> None:
        self.name = name
        self.loop()
    
    def loop(self):
        numDevices = self.count_connected_devices()



    def count_connected_devices(self):
        # Create an instance of the nmap.PortScanner
        nm = nmap.PortScanner()
    
        # Define the network range to scan
        # Change '192.168.1.0/24' if your IP range is different
        network_range = '192.168.1.0/24'
    
        print("Scanning network, please wait...")
        nm.scan(hosts=network_range, arguments='-sn')
    
        # Count devices with 'up' status (active on network)
        connected_devices = [host for host in nm.all_hosts() if nm[host].state() == 'up']
    
        print(f"Number of connected devices: {len(connected_devices)}")
        #for device in connected_devices:
        #    print(f"Device IP: {device}")
        return len(connected_devices) - NUM_STATIONS - 1


scanner = Station(STATION_NAME)
scanner.count_connected_devices()
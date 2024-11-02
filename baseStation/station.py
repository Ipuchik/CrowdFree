import nmap
import requests
import json
import time

NUM_STATIONS = 1
STATION_NAME = "SBBLT2-1"
STATION_ROOM = "SBBLT2"
API_ADDRESS = "http://ec2-18-132-37-221.eu-west-2.compute.amazonaws.com"#"http://127.0.0.1:8000"

ADDRESS_RANGE='172.16.17.59/22'#192.168.1.0/24

class Station:
    def __init__(self, name) -> None:
        self.name = name

        self.setup()

        while True:
            self.loop()

    def requestCreateRoom(self):
        print("We need to create a new room")
        print(f"Room Name: {STATION_ROOM}")
        roomCapacity = int(input("Room Capacity:  "))
        lat = float(input("Room Latitude:  "))
        long = float(input("Room Longitude:  "))
        
        data = {"name": STATION_ROOM,
                "latitude": lat,
                "longitude":long,
                "capacity":roomCapacity}

        response = requests.post(API_ADDRESS + "/addRoom", json=data)

        print(response.text)
    
    def setup(self):
        ## First check if room exists
        response = requests.get(API_ADDRESS+"/getRooms")
        response = json.loads(response.text)
        print(response)
        roomExists = False
        for room in response:
            name = room.get("RoomName")
            if name == STATION_ROOM:
                roomExists = True
                self.room = room
                break
        
        if not roomExists:
            print("ERROR: Room does not exist.")

            self.requestCreateRoom()


        ## Now register this station with the API
        reqData = {"name": STATION_NAME,
                   "roomName": STATION_ROOM}
        response = requests.post(API_ADDRESS+"/addStation", json=reqData)
        print(response.status_code)
        print(response.text)

        ## Now find our station id number        getStationByName
        response = requests.get(API_ADDRESS + f"/getStationByName/{STATION_NAME}")
        print(response.text)
        print(response.reason)
        self.station = json.loads(response.text)
        print(self.station)
    
    def loop(self):
        numDevices = self.count_connected_devices()
        data = {"numDevices": numDevices}
        response = requests.post(API_ADDRESS + f"/setNumDevices/{self.station.get('StationID')}", json=data)
        print(response.text)
        print(data)
        
        time.sleep(10)


    def count_connected_devices(self):
        # Create an instance of the nmap.PortScanner
        nm = nmap.PortScanner()
    
        # Define the network range to scan
        # Change '192.168.1.0/24' if your IP range is different
        network_range = ADDRESS_RANGE
    
        print("Scanning network, please wait...")
        nm.scan(hosts=network_range, arguments='-sn')
    
        # Count devices with 'up' status (active on network)
        connected_devices = [host for host in nm.all_hosts() if nm[host].state() == 'up']
    
        print(f"Number of connected devices: {len(connected_devices)}")
        #for device in connected_devices:
        #    print(f"Device IP: {device}")
        return len(connected_devices) - NUM_STATIONS - 1


scanner = Station(STATION_NAME)
import random
import ipaddress

class Device:
    def __init__(self, ip, signalStrength):
        self.ip = ip
        self.signalStrength = signalStrength
    
class DummyScanner:
    def __init__(self):
        pass

    def getConnectedDevices():
        devices = []
        for i in range(random.randint(0, 10)):
            dev = Device(ipaddress.ip_address(f"192.168.1.{random.randint(2, 255)}"))
            devices.append(dev)
        return devices
    
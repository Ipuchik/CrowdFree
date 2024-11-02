import time
import sys
from scanning import DummyScanner as Scanner

API_ADDRESS = ""

def main():
    scanner = Scanner()

    while True:
        devices = scanner.getConnectedDevices()



        time.sleep(5)

if __name__ == "__main__":
    print("start")
    main(sys.argv[0])
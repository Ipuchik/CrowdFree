from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
import sqlite3
import dbManager

database = dbManager.Database("database.db")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def getRooms(self):
        rooms = database.getRooms()
        print(rooms)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(rooms).encode())

    def getRoomFill(self, roomId):
        roomFill = database.getRoomFill(roomId)
        print(roomFill)
        
        if roomFill != None:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"RoomID": roomFill[0],
                        "NumDevices": roomFill[1]}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Room not found'}
            self.wfile.write(json.dumps(response).encode())

    def getStationByName(self, name):
        station = database.getStationByName(name)

        if station == None:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Station not found'}
            self.wfile.write(json.dumps(response).encode())
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(station).encode())


    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        print(path_parts)
        if self.path == '/getRooms':
            self.getRooms()
        elif path_parts[0] == "getStationByName" and len(path_parts) == 2:
            stationName = path_parts[1]
            self.getStationByName(stationName)
        elif path_parts[0] == 'getRoomInfo' and len(path_parts) == 2:
            room_id = path_parts[1]
            self.getRoomFill(room_id)
        else:
            self.send_response(404)
            self.end_headers()
            response = {'error': 'API endpoint doesnt exist'}
            self.wfile.write(json.dumps(response).encode())
    
    def addRoom(self, roomInfo):
        name = roomInfo.get("name")
        lat = roomInfo.get("latitude")
        long = roomInfo.get("longitude")
        capacity = roomInfo.get("capacity")

        if not lat or not long:
            lat = 0
            long = 0

        if capacity == None:
            capacity = -1

        if not name:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Missing name'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        database.addRoom(name, lat, long, capacity)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Room added successfully'}
        self.wfile.write(json.dumps(response).encode())
    
    def addStation(self, stationInfo):
        ## Contains stationName, latitude, longitude, roomName
        stationName = stationInfo.get("name")
        lat = stationInfo.get("latitude")
        long = stationInfo.get("longitude")
        roomName = stationInfo.get("roomName")

        if not lat or not long:
            lat = 0
            long = 0
        

        if not stationName:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Missing name'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        database.addStation(stationName, lat, long, roomName)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Station added successfully'}
        self.wfile.write(json.dumps(response).encode())
    
    def setNumDevices(self, stationId, data):

        numDevices = data.get("numDevices")

        validStationId = False
        if stationId:
            validStationId = database.getStationById(stationId) != None

        if not validStationId:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'StationId does not exist'}
            self.wfile.write(json.dumps(response).encode())
            return

        if not numDevices:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Missing numDevices'}
            self.wfile.write(json.dumps(response).encode())
            return
        
        database.setStationNumDevices(stationId, numDevices)

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Updated successfully'}
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            print(body)
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Invalid JSON'}
            self.wfile.write(json.dumps(response).encode())
            return

        if self.path == '/addRoom':
            self.addRoom(data)    
        elif self.path == "/addStation":
            self.addStation(data)
        elif path_parts[0] == 'setNumDevices' and len(path_parts) == 2:
            stationId = path_parts[1]
            self.setNumDevices(stationId, data)
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

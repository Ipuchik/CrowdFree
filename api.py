from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
import sqlite3
import dbManager

database = dbManager.Database()

# In-memory storage for rooms
rooms = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def getRooms(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = list(rooms.keys())
        self.wfile.write(json.dumps(response).encode())

    def getRoomInfo(self, roomId):
        if roomId in rooms:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = rooms[roomId]
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Room not found'}
            self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        if self.path == '/getRooms':
            self.getRooms()
        
        elif path_parts[0] == 'getRoomInfo' and len(path_parts) == 2:
            room_id = path_parts[1]
            self.getRoomInfo(room_id)
        else:
            self.send_response(404)
            self.end_headers()
    
    def addRoom(self, roomInfo):
        

        if not room_id or not room_info:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Missing room_id or room_info'}
            self.wfile.write(json.dumps(response).encode())
            return
        if room_id in rooms:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Room already exists'}
            self.wfile.write(json.dumps(response).encode())
            return
        rooms[room_id] = room_info
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Room added successfully'}
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
            
        
        elif path_parts[0] == 'setRoomInfo' and len(path_parts) == 2:
            room_id = path_parts[1]
            if room_id not in rooms:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Room not found'}
                self.wfile.write(json.dumps(response).encode())
                return
            room_info = data.get('room_info')
            if not room_info:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Missing room_info'}
                self.wfile.write(json.dumps(response).encode())
                return
            rooms[room_id] = room_info
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'Room info updated successfully'}
            self.wfile.write(json.dumps(response).encode())
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

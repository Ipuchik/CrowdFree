import sqlite3

SETUP_DB = """
CREATE TABLE IF NOT EXISTS ROOM (
    RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomName VARCHAR(40),
    Coordinates VARCHAR(30)
);
CREATE TABLE IF NOT EXISTS STATION (
    StationID INTEGER PRIMARY KEY AUTOINCREMENT,
    StationName VARCHAR(30),
    Coordinates VARCHAR(30),
    NumDevices INTEGER,
    LastRecording DATE,
    RoomID INTEGER FOREIGN KEY
);
"""

class Database:
    def __init__(self, fileName):
        self.dbFile = fileName
        self.conn = None
    
    def setup(self):
        self.conn = sqlite3.connect(self.dbFile)
        
        cursor = self.conn.cursor()

        cursor.execute()
        cursor.close()

    def addRoom(self, roomName, roomPosition):
        cursor = self.conn.cursor()

        cursor.execute(f"INSERT INTO ROOM (RoomName, RoomCoordinates) VALUES ({roomName, roomPosition})")
    
    def addStation(self, )
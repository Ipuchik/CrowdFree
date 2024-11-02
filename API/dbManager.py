import sqlite3

CREATE_ROOM_TABLE = """
CREATE TABLE IF NOT EXISTS ROOM (
    RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomName TEXT UNIQUE,
    RoomLat REAL,
    RoomLong REAL,
    RoomCapacity INTEGER
);"""
CREATE_STATION_TABLE = """
CREATE TABLE IF NOT EXISTS STATION (
    StationID INTEGER PRIMARY KEY AUTOINCREMENT,
    StationName TEXT UNIQUE,
    StationLat REAL,
    StationLong REAL,
    NumDevices INTEGER,
    LastRecording TEXT,
    RoomID INTEGER
);
"""

class Database:
    def __init__(self, fileName):
        self.dbFile = fileName
        self.setup()
    
    def setup(self):
        conn = sqlite3.connect(self.dbFile)
        
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor.execute(CREATE_ROOM_TABLE)
        cursor.execute(CREATE_STATION_TABLE)
        cursor.close()
        conn.commit()
        conn.close()
    
    def getRoomFill(self, roomId):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor = cursor.execute(f"""SELECT StationID, NumDevices FROM STATION
                                NATURAL JOIN ROOM""")
        result = cursor.fetchall()
        print(result)
        cursor.close()
        conn.close()

        if len(result) == 0:
            return [roomId,0]


        totalDevices = 0
        for v in result:
            if v[1] != None:
                totalDevices += v[1]
        result = [roomId, totalDevices]

        return result

    def addRoom(self, roomName, roomLat, roomLong, roomCapacity):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor = cursor.execute(f"""INSERT INTO ROOM (RoomName, RoomLat, RoomLong, RoomCapacity) 
                                VALUES (?,?,?,?)""", (roomName, roomLat, roomLong, roomCapacity))
        cursor.close()
        conn.commit()
        conn.close()
    
    def addStation(self, stationName, lat, long, roomName):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        try:
            cursor = cursor.execute(f"""INSERT INTO STATION (StationName, StationLat, StationLong, RoomID) 
                           VALUES (?,?,?,(SELECT RoomID FROM ROOM WHERE RoomName=?))""", (stationName, lat, long, roomName))
        
            
        except sqlite3.IntegrityError:
            ## Already exists: No problem
            pass
        finally:
            cursor.close()

            conn.commit()
            conn.close()

    def getRooms(self):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor = cursor.execute(f"""SELECT * FROM ROOM""")

        rooms = cursor.fetchall()
        res = []
        for room in rooms:
            room = {
                "RoomID": room[0],
                "RoomName": room[1],
                "RoomLat": room[2],
                "RoomLong": room[3],
                "RoomCapacity": room[4]
            }
            res.append(room)

        rooms = res
        cursor.close()
        conn.close()
        print(rooms)

        return rooms

    def getStationById(self, stationId):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor = cursor.execute(f"""SELECT * FROM STATION WHERE StationID=?""", [stationId])

        station = cursor.fetchone()

        cursor.close()
        conn.close()
        print(station)

        if len(station) == 0:
            return None
        
        station = {"StationID": station[0],
                   "StationName": station[1],
                   "StationLat": station[2],
                   "StationLong": station[3],
                   "NumDevices": station[4],
                   "LastRecording": station[5],
                   "RoomID": station[6]
                   }

        return station
    
    def getStationByName(self, stationName):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor = cursor.execute(f"""SELECT * FROM STATION WHERE StationName=?""", [stationName])

        station = cursor.fetchone()

        cursor.close()
        conn.close()
        print(station)

        if len(station) == 0:
            return None
        
        station = {"StationID": station[0],
                   "StationName": station[1],
                   "StationLat": station[2],
                   "StationLong": station[3],
                   "NumDevices": station[4],
                   "LastRecording": station[5],
                   "RoomID": station[6]
                   }
        
        return station
    
    def getRoomInfo(self, roomName):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor = cursor.execute(f"SELECT * FROM ROOM WHERE RoomName='?'", (roomName,))
        
        roomInfo = cursor.fetchone()
        print(roomInfo)

        cursor.close()
        conn.close()
        return roomInfo

    def getStationsInRoom(self, roomId):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor = cursor.execute(f"SELECT * FROM STATION WHERE RoomID=(?)", [roomId])

        stations = cursor.fetchall()
        print(stations)

        cursor.close()
        conn.close()
        return stations
    
    def setStationNumDevices(self, stationId, numDevices):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor = cursor.execute(f"""UPDATE STATION
                                SET NumDevices=(?) WHERE StationID=(?)""", [numDevices, stationId])
        
        cursor.close()
        conn.commit()
        conn.close()
        return True
from websocket import create_connection
import json
import time
import requests

class Chimera:
    def __init__(self, project_id, session_id, username):
        self.project_id = project_id
        self.length_limit = 256
        self.cloud_host = "wss://clouddata.scratch.mit.edu"
        self.cookie = "scratchsessionsid=" + session_id + ";"
        self.origin = "https://scratch.mit.edu"
        self.username = username
        self.ws = None
        self.reconnect_attempts = 3
        self.retry_delay = 2

    def connect(self):
        try:
            headers = {
                "Cookie": self.cookie,
                "Origin": self.origin
            }
            self.ws = create_connection(
                f"{self.cloud_host}",
                header=headers
            )
            handshake = {
                "method": "handshake",
                "user": self.username,
                "project_id": str(self.project_id)
            }
            self.ws.send(json.dumps(handshake) + "\n")
            print("Connected to Scratch Cloud WebSocket")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def reconnect(self):
        for attempt in range(self.reconnect_attempts):
            print(f"Reconnection attempt {attempt + 1}/{self.reconnect_attempts}")
            if self.connect():
                return True
            time.sleep(self.retry_delay)
        return False

    def set_var(self, variable, value):
        try:
            if not self.ws:
                if not self.reconnect():
                    raise Exception("Failed to reconnect")

            value = str(value)
            if len(value) > self.length_limit:
                raise Exception(f"Value exceeds length limit of {self.length_limit}")

            packet = {
                "method": "set",
                "name": "☁ " + str(variable),
                "value": value,
                "user": self.username,
                "project_id": str(self.project_id)
            }
            self.ws.send(json.dumps(packet) + "\n")
            time.sleep(0.1)  # Rate limit
            return True
        except Exception as e:
            print(f"Error setting variable: {e}")
            self.ws = None  # Reset connection
            return False

    def get_var(self, variable):
        try:
            logs = self.logs(limit=100)
            filtered = list(filter(lambda k: k["name"] == "☁ " + variable, logs))
            return filtered[0]["value"] if filtered else None
        except Exception as e:
            print(f"Error getting variable: {e}")
            return None

    def logs(self, limit=100):
        try:
            data = requests.get(
                f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit={limit}&offset=0",
                timeout=10
            ).json()
            return data
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return []

    def close(self):
        try:
            if self.ws:
                self.ws.close()
        except Exception as e:
            print(f"Error closing connection: {e}")

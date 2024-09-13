# event.py

class Event:
    def __init__(self, data):
        self.type = data.get('type')
        self.data = data.get('data')
        self.timestamp = data.get('timestamp')

# role.py

class Role:
    def __init__(self, data):
        self.id = data.get('role_id')
        self.name = data.get('role_name')

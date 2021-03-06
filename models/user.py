from flask_login import UserMixin
from .role import Role

class User(UserMixin):
    def __init__(self, id, active=True, role=Role.READER):
        self.id = id
        self.active = active
        self.role = role

    def is_active(self):
        return self.active
    
    def get_id(self):
        return self.id

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active
    
    def get_id(self):
        return self.id

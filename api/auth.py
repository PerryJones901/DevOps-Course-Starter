import os

from flask_login import current_user
from models.role import Role
from models.user import User

def get_user(user_id) -> User:
    return User('name', user_id)

def requires_role(role: Role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_user(current_user.get_id())
            if(authorisation_disabled() or user.role is role):
                return func(*args, **kwargs)
            else:
                return 'Not Authorized'
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

def authorisation_disabled() -> bool:
    print(os.environ.get('LOGIN_DISABLED') == "True")
    return os.environ.get('LOGIN_DISABLED') == "True"

from werkzeug.security import safe_str_cmp

from user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    #print(user)
    if user and safe_str_cmp(user.password, password):
        print(user.password)
        return user
#authenticate("bob","asdf")

def identity(payload):
    user_id = payload["identity"]
    #print(user_id)
    return User.find_by_id(user_id)
#identity(payload)

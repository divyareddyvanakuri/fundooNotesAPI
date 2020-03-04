import jwt
import datetime
import time
def tokenActivation(username,password):
    payload = {
        'username': username,
        'password': password,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }
    # time.sleep(32)
    token = jwt.encode(payload, 'SECRET_KEY').decode('utf-8')
    return token
def passwordActivation(username):
    payload = {
        'username': username
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }
    # time.sleep(32)
    token = jwt.encode(payload, 'SECRET_KEY').decode('utf-8')
    return token
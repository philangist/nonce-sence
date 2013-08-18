import time
import md5
from functools import wraps
from bottle import (
    get,
    abort,
    request,
    run
)

NONCE_LIST = []
SECRET_PASSWORD = 'Ill send an SOS to the world'


def get_secret_password(username):
    if username == 'phil':
        return SECRET_PASSWORD
    return 'None'


def check_auth(username, password):
    try:
        nonce = NONCE_LIST.pop()
    except IndexError:
        return False
    secret_password = get_secret_password(username)
    expected_hash = md5.new(nonce + secret_password)
    secret_password = expected_hash.hexdigest()
    if not password == secret_password:
        return False
    return True


def authenticate():
    abort(401, 'Could not verify your access level for that URL.')


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.auth
        if not auth or not check_auth(auth[0], auth[1]):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@get('/nonce')
def get_nonce():
    nonce = str(time.time())
    NONCE_LIST.append(nonce)
    print nonce
    return nonce


@get('/hello')
@requires_auth
def hello():
    return 'HELLO WORLD!'


if __name__ == '__main__':
    run(host='localhost', port='4000')


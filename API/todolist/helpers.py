from functools import wraps
# from pickle import FALSE
from flask import jsonify, request
# from flask_login import current_user
from todolist.models import User
import jwt
from todolist import app
import time

# token required decorator for task view
## help from https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        print('auth headers: ' + str(auth_headers))

        invalid_msg = {
            'message': 'Invalid token, authentication required.',
            'Authenticated': False,
            'status': 401
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'Authenticated': False,
            'status': 401
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg)

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data['exp'] > time.time())
            user = User.query.filter_by(username=data['sub']).first()
            print(user)
            if not user:
                raise RuntimeError('User not found.')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg)
        except (jwt.InvalidTokenError, Exception) as e:
            print('error - ' + str(e))
            return jsonify(invalid_msg)

    return _verify

def validate_username(username_to_check):
    user = User.query.filter_by(username=username_to_check).first()
    if user:
        return False
    else:
        return True

def validate_email_address(email_address_to_check):
    email = User.query.filter_by(email=email_address_to_check).first()
    if email:
        return False
    else:
        return True


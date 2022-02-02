from functools import wraps
# from pickle import FALSE
from flask import jsonify, request
# from flask_login import current_user
from todolist.models import User
import jwt
from todolist import app

# token required decorator for task view
## help from https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        print(auth_headers)

        invalid_msg = {
            'message': 'Invalid token, authentication required.',
            'Authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'Authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found.')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

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


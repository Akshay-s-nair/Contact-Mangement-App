# utils.py

from functools import wraps
from flask import request, jsonify
import jwt
from models import User, TokenBlacklist
from config import Config

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        blacklisted_token = TokenBlacklist.query.filter_by(token=token).first()
        if blacklisted_token:
            return jsonify({'error': 'Token has been revoked'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['user_pid']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return func(current_user, *args, **kwargs)

    return decorated

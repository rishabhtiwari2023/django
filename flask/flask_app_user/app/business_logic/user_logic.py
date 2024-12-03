from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity
from ..models import User, UserGroup,Log
from ..decorators import role_required
# from db import db
import logging
from datetime import datetime
from .. import db

logger = logging.getLogger(__name__)

def register_user(data):
    if not data or not data.get('username') or not data.get('password') or not data.get('role'):
        return {"msg": "Invalid input"}, 400

    # Check if the username already exists
    if User.query.filter_by(username=data['username']).first():
        return {"msg": "Username already exists"}, 409

    hashed_password = generate_password_hash(data['password'], method="pbkdf2:sha256", salt_length=8)

    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    logger.info(f"User {new_user} registered successfully.")
    save_log(new_user.id, "User registered successfully.", "INFO")
    return {"msg": "User registered successfully"}, 201

def login_user(data):
    if not data or not data.get('username') or not data.get('password'):
        return {"msg": "Invalid input"}, 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return {"msg": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.id)
    return {"user_id": user.id, "access_token": access_token}, 200

def get_user_info(user_id):
    user = User.query.get(user_id)
    return {"username": user.username, "role": user.role}

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404
    db.session.delete(user)
    db.session.commit()
    return {"msg": "User deleted successfully"}, 200

def save_log(user_id, message, level):
    log_entry = Log(user_id=user_id, message=message, level=level, timestamp=datetime.utcnow())
    db.session.add(log_entry)
    db.session.commit()
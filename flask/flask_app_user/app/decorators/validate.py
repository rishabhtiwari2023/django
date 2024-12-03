from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..models import User, Log
import logging
from .. import db
logger = logging.getLogger(__name__)

def save_log(user_id, message, level):
    log = Log(user_id=user_id, message=message, level=level)
    db.session.add(log)
    db.session.commit()

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user is None:
                message = f"User not found: {user_id}"
                logger.error(message)
                save_log(user_id, message, "ERROR")
                return {"msg": "User not found"}, 404
            if user.role != role:
                message = f"Permission denied for user: {user_id}"
                logger.warning(message)
                save_log(user_id, message, "WARNING")
                return {"msg": "Permission denied"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
import logging
from flask import request, jsonify, make_response, session as flask_session
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..middleware.middleware import validate_input
from ..business_logic import register_user, login_user, get_user_info, delete_user,save_log
from ..decorators import role_required
from ..models import UserGroup, Session
from .. import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_session(user_id, session_data):
    session = Session(user_id=user_id, session_data=session_data)
    db.session.add(session)
    db.session.commit()

def initialize_routes(app):
    api = Api(app)

    @app.route('/register', methods=['POST'], endpoint='register')
    @validate_input(['username', 'password', 'role'])
    def register():
        data = request.get_json()
        response, status = register_user(data)
        return make_response(jsonify(response), status)

    @app.route('/login', methods=['POST'], endpoint='login')
    @validate_input(['username', 'password'])
    def login():
        data = request.get_json()
        response, status = login_user(data)
        if status == 200:
            if 'user_id' in response:
                flask_session['user'] = response['user_id']
                access_token = create_access_token(identity=response['user_id'])
                logger.info(f"User {response['user_id']} logged in successfully.")
                save_log(response['user_id'], "User logged in successfully.", "INFO")
                save_session(response['user_id'], str(flask_session))
                return make_response(jsonify(access_token=access_token), status)
            else:
                logger.error("Login response missing 'user_id'")
                return make_response(jsonify({"msg": "Login failed, user_id missing"}), 500)
        else:
            logger.error(f"Failed login attempt for username: {data['username']}")
            save_log(None, f"Failed login attempt for username: {data['username']}", "ERROR")
            return make_response(jsonify(response), status)
        
    @app.route('/fetch_user',methods=['GET'],endpoint='fetch_user')
    # def fetch_user():


    class UserManagement(Resource):
        @jwt_required()
        def get(self):
            user_id = get_jwt_identity()
            response = get_user_info(user_id)
            return make_response(jsonify(response))

        @role_required(UserGroup.ADMIN)
        def delete(self, user_id):
            response, status = delete_user(user_id)
            return make_response(jsonify(response), status)
    # class OrganisatioinManagement(Resource):
    #     @jwt_required()
    #     def get(self):
    #         response=get_all_organisation()
    #         return make_response(jsonify(response))
               

    api.add_resource(UserManagement, '/user', '/user/<int:user_id>')
    # api.add_response(OrganisatioinManagement,'/organisations','/organisation/<int:organisation_id>')
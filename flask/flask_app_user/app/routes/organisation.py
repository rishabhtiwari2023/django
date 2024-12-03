import logging
from flask import request, jsonify, make_response, session as flask_session
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..middleware.middleware import validate_input
from ..business_logic import register_user, login_user, get_user_info, delete_user,save_log
from ..decorators import role_required
from ..models import UserGroup, Session

from .. import db    class OrganisatioinManagement(Resource):
        @jwt_required()
        def get(self):
            response=get_all_organisation()
            return make_response(jsonify(response))
               
    api.add_response(OrganisatioinManagement,'/organisations','/organisation/<int:organisation_id>')
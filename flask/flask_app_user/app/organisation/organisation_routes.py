from flask import Blueprint, session, Response, request, jsonify
from .. import db
from .organisation_modals import *
from .forms import OrganisationForm

organisation = Blueprint('organisation', __name__)

@organisation.route('/organisations1', methods=['GET'])
def get_all_organisation():
    print(request.remote_addr)  # Print client IP address
    print(request.headers)  # Print all client headers
    organisations = Organisation.query.all()
    return Response("organisations")

@organisation.route('/organisation/<int:organisation_id>', methods=['GET'])
def get_organisation(organisation_id):
    try:
        organisation = Organisation.query.filter_by(organisation_id=organisation_id).first()
        return jsonify({"organisation": organisation})
    except Exception as e:
        return jsonify({"error": "there is an error in fetching the organisation"})

@organisation.route("/organisation", methods=['POST'])
def add_organisation():
    data = request.get_json()
    # Add your code here

    return Response("organisations")

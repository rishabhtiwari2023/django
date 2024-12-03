from flask import Flask
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from .db import db
import os
# from .routes import user_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .organisation.organisation_routes import organisation
# db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['JWT_SECRET_KEY'] = '_jwt_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'  # Replace with a unique and secret key
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
    from .routes import initialize_routes
    initialize_routes(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return str(user_id)  # Ensure the subject is a string


    app.register_blueprint(organisation)
    return app

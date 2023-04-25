
from flask import Flask, render_template, url_for,flash,redirect,request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
#from flask_mail import Mail
from app.config import Config
import os
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
# Initialize Flask App  C:\new services\RDV_S\project\app\key.json




cred = credentials.Certificate('C:/RDV_S/project/app/key.json')
default_app = initialize_app(cred)
db = firestore.client()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")

   
    bcrypt.init_app(app)
    
    
    
    from app.entity.Participant.route import participant
    from app.entity.Piece.route import piece
    from app.entity.Rubrique.route import rubriq
    from app.entity.Cles.route import cles
    from app.entity.Compteur.route import compteur
    from app.entity.Extension.route import extenssion
    from app.entity.Voie.route import voie
    from app.entity.User.route import user
    from app.entity.Client.route import client
    
    
    
    app.register_blueprint(participant)
    app.register_blueprint(piece)
    app.register_blueprint(rubriq)
    app.register_blueprint(cles)
    app.register_blueprint(compteur)
    app.register_blueprint(extenssion)
    app.register_blueprint(voie)
    app.register_blueprint(user)
    app.register_blueprint(client)
    
    return app
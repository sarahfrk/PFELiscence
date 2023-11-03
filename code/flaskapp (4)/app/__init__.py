from flask import Flask,jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message


from flask_cors import CORS, cross_origin



app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


app.secret_key = "griqgiq yrgutgezrizterihz gygryir"
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:''@localhost/hammadb'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:''@localhost/hammadbsarah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

CORS(app)



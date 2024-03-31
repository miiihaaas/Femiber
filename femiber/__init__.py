from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_mail import Mail
# from dotenv import load_dotenv
import os


# load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b0f805f651d04f909f539ec57f8a89c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_APP'] = 'run.py'

db = SQLAlchemy(app)

app.config['JSON_AS_ASCII'] = False #! da ne bude ascii već utf8


from femiber.main.routes import main


app.register_blueprint(main)
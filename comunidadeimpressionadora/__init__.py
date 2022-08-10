from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"]='2e4fc1775db26ec887ed3262d48bb89a'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///comunidade.db"

database = SQLAlchemy(app)
bcrypt=Bcrypt(app)
loginmanager=LoginManager(app)
loginmanager.login_view="login"
loginmanager.login_message_category="alert-info"

from comunidadeimpressionadora import routes
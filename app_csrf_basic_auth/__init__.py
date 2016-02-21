from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_path=None, static_url_path=None, static_folder='static', template_folder='templates', instance_path=None, instance_relative_config=False)

app.config["SECRET_KEY"] = "super secret"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'

db = SQLAlchemy(app=app, use_native_unicode=True, session_options=None, metadata=None)

from . import views


import os
import psycopg2
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
login = LoginManager()

login.login_view = 'login_register'

app.config['SECRET_KEY'] = 're:zero'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("postgres", "postgresql")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
login.init_app(app)

from models import User

with app.app_context():
    db.create_all()
    if db.session.query(User).filter_by(username='Bodya').count() == 0:
        user_ = User(username='Bodya')
        user_.set_password("password")
        db.session.add(user_)
    db.session.commit()


# Import module with routes
import routes

import os
from flask import Flask
from flask_bcrypt import Bcrypt
import secrets
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
     
app = Flask(__name__)
# set base Directory
basedir = os.path.abspath(os.path.dirname(__file__))
# create the secret_key_hash
secret_key = secrets.token_hex(16)
bcrypt = Bcrypt(app)
secret_key_hash = bcrypt.generate_password_hash(secret_key)
# Database configuration
app.config['SECRET_KEY'] = secret_key_hash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=30)
# build database
db = SQLAlchemy(app)
Migrate(app,db)


from .views import views
from .auth import auth
#from .tripdist import tripdist
#from .tripass import tripass
#from .eetrip import eetrip
#from .me import me
#from .shortpath import shortpath

# create the Views Blueprint
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
#app.register_blueprint(tripdist, url_prefix='/')
#app.register_blueprint(tripass, url_prefix='/')
#app.register_blueprint(eetrip, url_prefix='/')
#app.register_blueprint(me, url_prefix='/')
#app.register_blueprint(shortpath, url_prefix='/')

    

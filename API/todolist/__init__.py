from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_cors import CORS
import logging

# initialize app, db, session, hash function, login, admin
app = Flask(__name__, static_url_path='/todolist/static')

# # GCP DB CREDENTIALS
# PASSWORD ="theBusiness"
# PUBLIC_IP_ADDRESS ="34.145.154.60"
# DBNAME ="todolist-db"
# INSTANCE_NAME ="barker-todolist:us-east4:todolist-db"
 
# # configuration

# app.config["SQLALCHEMY_DATABASE_URI"]= f'postgresql+psycopg2://kwkbarker:{PASSWORD}@/{DBNAME}?host={PUBLIC_IP_ADDRESS}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False


# SQLITE DB VERSION

app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///sqlitedb.db'

# initialize database
db = SQLAlchemy(app)
db.drop_all()
db.create_all()



# enable CORS
cors = CORS(app, resources=r'/api/*', send_wildcard=True, origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'
logging.getLogger('flask_cors').level = logging.DEBUG

app.config['SECRET_KEY'] = '5475298b378974fc7aa4f496'

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.init_app(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, template_mode='bootstrap3')


from todolist.routes import api
app.register_blueprint(api, url_prefix="/api")

from todolist import routes

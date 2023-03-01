from flask import Flask, Blueprint
from .config_parser import Config
from flask_migrate import Migrate
from flask_discord import DiscordOAuth2Session
from .models import db

site = Flask(__name__)

# Site config
config = Config().__dict__
site.config["SECRET_KEY"] = config["secret_key"]
# Set discord values
site.config["DISCORD_CLIENT_ID"] = config["config"]["discord"]["client_id"]
site.config["DISCORD_CLIENT_SECRET"] = config["config"]["discord"]["client_secret"]
site.config["DISCORD_REDIRECT_URI"] = config["config"]["discord"]["redirect_uri"]
# Set DB Values
site.config["SQLALCHEMY_DATABASE_URI"] = config["config"]["mysql"]
site.config["SQLALCHEMY_TRACK_MODIFCATIONS"] = config["config"]["mysql_track_modifications"]


discord = DiscordOAuth2Session(site)

from . import routes
from .upload.routes import upload
from .auth.routes import auth
from .admin.routes import admin
serve_storage = Blueprint('files', __name__, static_folder='storage')
site.register_blueprint(upload)
site.register_blueprint(auth)
site.register_blueprint(admin)
site.register_blueprint(serve_storage)

db.init_app(site)
migrate = Migrate(site, db)
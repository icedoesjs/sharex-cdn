from flask import Flask, Blueprint
import os
from config.ConfigParser import load_config
from flask_discord import DiscordOAuth2Session
from flask_migrate import Migrate
from app.models import db
import secrets

class ShareXCDN(Flask):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config_file = load_config(os.path.abspath(os.path.join(os.getcwd(), 'config', 'config.yaml')))
    
    def setup(self) -> None:
        # Build connection string for MySql
        self.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + self.config_file['mysql']['user'] + f':{self.config_file["mysql"]["password"]}' + f'@{self.config_file["mysql"]["host"]}/' + self.config_file["mysql"]["database"]
        self.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
        # Set all discord variables
        self.config['DISCORD_CLIENT_ID'] = self.config_file['discord']['client_id']
        self.config['DISCORD_CLIENT_SECRET'] = self.config_file['discord']['client_secret']
        self.config['DISCORD_REDIRECT_URI'] = self.config_file['discord']['redirect_uri']
        # Set secret key
        self.config['SECRET_KEY'] = secrets.token_urlsafe(16)
        
        os.environ["ROOT"] = os.getcwd()
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = str(self.config_file['insecure_transport'])
        # Future plans to heavily utilize this subclass for a lot of methods, like it should have been wrote.


site = ShareXCDN(__name__)
site.setup()
discord = DiscordOAuth2Session(site)

# Routes
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

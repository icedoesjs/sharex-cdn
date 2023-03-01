import yaml
import secrets 
import os


config_path = os.path.abspath(os.path.join(os.getcwd(), 'config', 'config.yaml'))
key = secrets.token_urlsafe(16)
with open(config_path) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
os.environ["ROOT"] = os.path.abspath(os.path.dirname(__name__))
# In production this must be removed
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

# Config class
class Config():
    def __init__(self):
        self.config = config 
        self.secret_key = key
import secrets
from app.models import Admins
import requests
import sys
import json

def generateAuthKey():
    key = secrets.token_urlsafe(10)
    while isDuplicate(key):
        key = secrets.token_urlsafe(10)
    return key

def validKey(key):
    search = Admins.query.filter(Admins.auth.in_([key])).all()
    if not search:
        return False
    else:
        return True

def isDuplicate(key):
    search = Admins.query.filter(Admins.auth.in_([key])).all()
    if not search:
        return False 
    else: 
        return True

def validUser(id):
    search = Admins.query.filter(Admins.user_id.in_([id])).all()
    if not search:
        return False
    else:
        return True

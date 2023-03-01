from flask import session
from app.models import Admins
from app import discord

def setAdmins():
    admins = Admins.query.all()
    all_admins = []
    for a in admins:
        all_admins.append(int(a.user_id))
    session['admins'] = all_admins

def isAdmin(user):
    check = Admins.query.filter(Admins.user_id.in_([user.id])).all()
    if not check:
        return False
    else:
        return True
    
def checkPerms(user):
    check = Admins.query.filter(Admins.user_id.in_([user.id])).all()
    if not check or int(check[0].permlevel) != 1: 
        return False
    else: 
        return True
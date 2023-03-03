from flask import Blueprint, redirect, url_for, render_template
from app import discord 

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route("/login")
def login():
    return discord.create_session()

@auth.route('/logout')
def logout():
    discord.revoke()
    return redirect(url_for('index'))

@auth.route('/callback')
def callback():
    data = discord.callback()
    redirect_to = data.get('redirect', '/')
    return redirect(redirect_to)

@auth.route('/unauthorized')
def unauthorized():
    return render_template('unauth.html')


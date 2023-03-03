from app import site, discord
from flask import render_template, redirect, url_for, session, request, send_from_directory
from .models import Settings, Admins
from flask_discord import Unauthorized
import os
import fnmatch
import time
from urllib.parse import urlparse

# Index Route
@site.route('/')
@site.route('/home')
@site.route('/index')
def index():
    if discord.authorized:
        url = urlparse(request.base_url)
        domain = url.netloc
        settings = Settings.query.get(1)
        if not settings:
            return print("The settings table has not been created. Please run source.sql")
        admins = Admins.query.all()
        if not admins:
            return print('The Admins table has not been created. Please run source.sql"')
        user = discord.fetch_user()
        session['pfp'] = user.avatar_url 
        session['u_id'] = user.id 
        site_admins = []
        # Set all site admins
        for u in admins:
            if int(u.permlevel) == 1:
                site_admins.append(int(u.user_id))
        session["admins"] = site_admins 
        # Get all settings
        session["name"] = settings.name 
        session["description"] = settings.description
        session["webhook"] = settings.webhook
        admin = Admins.query.filter(Admins.user_id.in_([str(user.id)])).all()
        if not admin:
            return redirect('auth.unauthorized')
        files = get_files(str(user.id))
        key = admin[0].auth
        return render_template('index.html', size=get_total_size(str(user.id)), total=get_total_files(str(user.id)), files=files, u_id=str(user.id), auth=key)
    else:
        return redirect(url_for('auth.login'))


# No login
@site.errorhandler(Unauthorized)
def unauth(e):
    return redirect(url_for('index'))

# 404
@site.errorhandler(404)
def four_o_four(e):
    return render_template('404.html', error='The page you attempted to access does not exist.')

@site.errorhandler(500)
def server_error(e):
    error = getattr(e, "original_exception", None)
    if error is None:
        return render_template('500.html', error='A 500 (Internal Server Error) occurred. The site has sorted the error and this seems to be an abort error.')
    return render_template('500.html', error=f'Internal Error: {error}')

def get_total_files(id):
    cwd = os.getcwd()
    dir = os.path.join(cwd, 'storage', id)
    count = len(fnmatch.filter(os.listdir(dir), '*.*'))
    return count

def get_total_size(id):
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, 'storage', id)):
        os.makedirs(os.path.join(cwd, 'storage', id))
    dir = os.path.join(cwd, 'storage', id)
    size = 0
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            fp = os.path.join(dir, f)
            if not os.path.islink(fp):
                size += os.path.getsize(fp)
    size = size/1048576
    return f"{round(size, 2)}MB"

def get_files(id):
    cwd = os.getcwd()
    dir = os.path.join(cwd, 'storage', id)
    files = {}
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            file = os.path.join(dir, f)
            if not os.path.islink(f):
                modify_date = os.path.getmtime(file)
                m_ti = time.ctime(modify_date)
                t_obj = time.strptime(m_ti)
                stamp = time.strftime("%Y-%m-%d", t_obj)
                file_size = os.path.getsize(file)
                mb_size = file_size/1048576
                name = f.split(".")[0]
                files[name] = {}
                files[name]["size"] = str(round(mb_size, 2)) + "MB" 
                files[name]["created"] = stamp
                files[name]["url"] = make_url(f, id)
                files[name]["ext"] = f.split(".")[1]
                files[name]["type"] = get_type(f)
                
    return files

def make_url(filename, userid):
    base = request.base_url
    if 'index' in base:
        base = request.base_url.split("index")[0]
    return base + f"storage/{userid}/{filename}"

def get_type(filename):
    images = ['jpg', 'png', 'jpeg', 'gif']
    file = ['txt']
    audio = ["wav", "mp3"]
    code = ["py", "js", "php", "ts", "cpp", "html", "cs", "json", "css", "sql", "asm"]
    video = ["mov", "mp4"]
    folder = ["zip", "rar", "7z"]
    extension = filename.split(".")[1]
    if extension in images:
        return 'image'
    elif extension in file:
        return 'text'
    elif extension in audio:
        return 'audio'
    elif extension in code:
        return 'code'
    elif extension in video:
        return 'video'
    elif extension in folder:
        return 'folder'
    else:
        return 'unknown'

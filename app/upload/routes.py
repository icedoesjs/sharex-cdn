import html
from app import discord, site
from flask import Blueprint, url_for, render_template, redirect, request, send_file, abort
from .forms import UploadFile
from app.core.Webhook import SendWebhook
from app.core.Auth import validKey, validUser
from app.core.Admin import isAdmin
from app.models import Admins, Settings
import os
from PIL import Image
import secrets
import fnmatch
import datetime

upload = Blueprint('upload', __name__, template_folder='upload_templates')
image_extentions = [".png", ".jpeg", ".jpg", ".gif"]
audio_extensions = [".wav", ".mp3"]
code_extensions = [".py", ".js", ".php", ".ts", ".cpp", ".html", '.cpp', ".cs", ".json", ".css", ".sql", ".asm", ".c", ".rs", ".md"]
video_extensions = [".mov", ".mp4"]
folder_extensions = [".zip", ".rar", ".7z"]


@upload.route('/manual/upload', methods=['GET', 'POST'])
def upload_manual():
    '''
    The route used for manual uploads.
    '''
    user = discord.fetch_user()
    if not isAdmin(user): return redirect('auth.unauthorized') 
    form = UploadFile()
    if request.method == 'POST':
        if form.validate():
            file_name = form.file.data.filename
            file_ext = os.path.splitext(file_name)[1]
            user_db = Admins.query.filter_by(user_id=str(user.id)).first()
            cwd = os.getcwd()
            if not os.path.exists(os.path.join(cwd, 'storage', str(user.id))):
                os.makedirs(os.path.join(cwd, 'storage', str(user.id)))
            if check_total_files(str(user.id)) > int(user_db.storagesize):
                abort(401, description='Your file limit has been reached.')
            fname = secrets.token_urlsafe(7)
            form.file.data.save(os.path.join(cwd, 'storage', str(user.id), fname + file_ext))
            # Best way i know how to do this is save the file and read size, if too large then delete and abort
            direct_file = request.files['file']
            if os.fstat(direct_file.fileno()).st_size > 6000000:
                os.remove(os.path.join(cwd, 'storage', str(user.id), f"{fname + file_ext}"))
                abort(401, description='The file you uploaded is too large.')
            settings = Settings.query.get(1)
            site_webhook = settings.webhook
            if file_ext in image_extentions:
                SendWebhook(site_webhook, request.base_url.split("upload")[0], 'New Upload', 'Image Uploaded', '1e90ff', f'A new image was uploaded by **{user.id}** to **storage/{user_db.folder_name}/{fname}{file_ext}**.', get_url(fname, user_db.user_id, file_ext))
            else:
                SendWebhook(site_webhook, request.base_url.split("upload")[0], 'New Upload', 'File Uploaded', '1e90ff', f'``{file_name}`` was uploaded by **{user.id}** to **storage/{user_db.folder_name}/{fname}{file_ext}**')
            return redirect(url_for('index'))
    return render_template('manual_upload.html', form=form)


@upload.route('/upload', methods=['POST'])
def upload_sharex():
    '''
    The route ShareX will post to.
    '''
    attr = request.form.to_dict(flat=False)
    if not validKey(attr['auth'][0]): return f"{attr['auth'][0]} is not a valid auth key.", 401
    if not validUser(attr['user'][0]): return f"{attr['user'][0]} is not a valid user.", 401
    file = request.files['file']
    og_name = file.filename
    file.flush()
    extension = os.path.splitext(file.filename)[1]
    if os.fstat(file.fileno()).st_size > 6000000:
        return 'File is too large.', 400
    
    user = Admins.query.filter(Admins.user_id.in_([attr['user'][0]])).all()
    user = user[0]
    settings = Settings.query.get(1)
    site_webhook = settings.webhook

    if extension in image_extentions:
        # Remove Metadata
        image = Image.open(file)
        data = list(image.getdata())
        remove_data = Image.new(image.mode, image.size)
        remove_data.putdata(data)
        # Save Image
        fname = secrets.token_urlsafe(7)
        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, 'storage', attr['user'][0])):
            os.makedirs(os.path.join(cwd, 'storage', attr['user'][0]))
        if check_total_files(attr['user'][0]) > int(user.storagesize):
            return 'Your file limit has been reached.', 401
        remove_data.save(os.path.join(cwd, 'storage', attr['user'][0], fname + extension))
        SendWebhook(site_webhook, request.base_url.split("upload")[0], 'New Upload', 'Image Uploaded', '1e90ff', f'A new image was uploaded by **{user.user_id}** to **storage/{user.folder_name}/{fname}{extension}**.', get_url(fname, user.user_id, extension))
        return get_url(fname, attr['user'][0], extension), 200
    elif extension == '.txt' or extension in code_extensions or extension in video_extensions or extension in folder_extensions or extension in audio_extensions:
        cwd = os.getcwd()
        fname = secrets.token_urlsafe(7)
        if not os.path.exists(os.path.join(os.getcwd(), 'storage', attr['user'][0])):
            os.makedirs(os.path.join(os.getcwd(), 'storage', attr['user'][0]))
        if check_total_files(attr['user'][0]) > int(user.storagesize):
            return 'Your file limit has been reached.', 401
        file.save(os.path.join(cwd, 'storage', attr['user'][0], fname + extension))
        SendWebhook(site_webhook, request.base_url.split("upload")[0], 'New Upload', 'File Uploaded', '1e90ff', f'``{og_name}`` was uploaded by **{user.user_id}** to **storage/{user.folder_name}/{fname}{extension}**')
        return get_url(fname, attr['user'][0], extension), 200
    else:
        return f"{extension} is not a file that can be uploaded on this server.", 401


@upload.route('/storage/<user_id>/<file>')
def get_image(user_id, file):
    '''
    The route used to fetch and return files when requested.
    '''
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, 'storage', user_id, file)):
        return render_template('not_supported.html', text='The file requested was not found')\
    # File exists, continue on
    file = os.path.join(cwd, 'storage', user_id, file)
    ext = os.path.splitext(file)[1]
    name = os.path.basename(file)
    # This could 100% be cleaned up, but it does indeed work lol
    if ext in image_extentions:
        return send_file(file)
    elif ext in audio_extensions or ext in video_extensions or ext == '.txt' or ext in folder_extensions:
        return send_file(file)
    elif ext == ".html":
        html_file = open(file)
        code = html_file.readlines()
        html_file.close()
        code.insert(0, '\n <!-- This HTML document has been beautified by the CDN. -->\n')
        return render_template('code.html', code=html.escape(''.join(code)), file=name, type="xml")
    elif ext == ".c":
        code_f = open(file, encoding='utf8')
        code = code_f.readlines()
        code_f.close()
        code.insert(0, '\n // This C file formatting may be different then the original upload, the CDN has attempted to correct mistakes in formatting.\n')
        return render_template('code.html', code=''.join(code), file=name, type="h")
    elif ext in code_extensions:
        code_f = open(file, encoding='utf8')
        code = code_f.readlines()
        code_f.close()
        code.insert(0, '\n')
        return render_template('code.html', code=''.join(code), file=name, type=ext.split(".")[1])
    else:
        return render_template('not_supported.html', text=f'If you would like support for {file} files, please open an issue on the Github repo.')


@upload.route('/delete/file/<name>/<ext>/<user_id>')
def delete_file(name, ext, user_id):
    '''
    The route used to delete files.
    '''
    cwd = os.getcwd()
    file = os.path.join(cwd, 'storage', user_id, name + "." + ext)
    os.remove(file)
    return redirect(url_for('index'))

def get_url(filename, userid, ext):
    '''
    A small internal function used to fetch file links
    '''
    if "manual" in request.base_url:
        base = request.base_url.split("manual")[0]
    else:
        base = request.base_url.split("upload")[0]
    return base + f"storage/{userid}/{filename}{ext}"

def check_total_files(u_id):
    '''
    Used to check a total number of files in a user's storage.
    '''
    cwd = os.getcwd()
    dir = os.path.join(cwd, 'storage', u_id)
    count = len(fnmatch.filter(os.listdir(dir), '*.*'))
    return count

def format_title(title: str, file):
    '''
    Format the title of the embed
    
    Params:
        title (str): The title of the embed from the config
        file: The file path of the current file we are creating a page for.
    '''
    ext = os.path.splitext(file)[1]
    name = os.path.basename(file)
    size = os.path.getsize(file) / 1024
    date = os.path.getmtime(file)
    variables = {'%fs': f'{size:.2f} MB', '%fd': f'{datetime.datetime.fromtimestamp(date)}', '%ft': ext, '%fne': name + ext, '%fn': name}
    for v in variables.keys():
        if v in title:
            title = title.replace(v, variables[v])
    return title

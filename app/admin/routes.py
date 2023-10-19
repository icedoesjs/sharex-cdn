from flask import Blueprint, redirect, url_for, render_template, session, request, flash, abort
from app import discord 
from flask_discord import requires_authorization
from app.core.Admin import isAdmin, checkPerms
from .forms import ChangeSettings, AddAdmin
from app.models import Settings, Admins
from app.core.Auth import generateAuthKey
from app.core.Webhook import sendInit

admin = Blueprint('admin', __name__, template_folder='admin_templates')

@admin.route('/admin', methods=['GET', 'POST'])
@requires_authorization
def admin_settings():
    user = discord.fetch_user()
    if not isAdmin(user): return redirect(url_for('index'))
    if not checkPerms(user): return redirect(url_for('index'))
    form = ChangeSettings()
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            desc = form.description.data
            webhook = form.webhook.data
            if (len(name) > 25): return flash('name is greater than 25')
            if (len(desc) > 250): return flash('description greater than 250')
            testHook = True
            if not webhook == session['webhook']: testHook = sendInit(webhook, session, request.base_url.split("admin")[0])
            if testHook:
                settings = Settings.query.get(1)
                settings.name = name 
                settings.description = desc 
                settings.webhook = webhook
                settings.update()
                return redirect(url_for('index'))
            else:
                return abort(500, description="Webhook is invalid")
    form.name.data = session['name']
    form.description.data = session['description']
    form.webhook.data = session['webhook']
    if not session['webhook']: form.webhook.data = 'No Webhook URL active'
    return render_template('admin.html', form=form)

@admin.route('/admin/users')
@requires_authorization
def admin_users():
    user = discord.fetch_user()
    if not isAdmin(user): return redirect(url_for('index'))
    if not checkPerms(user): return redirect(url_for('index'))
    admins = Admins.query.all()
    all_admins = {}
    for a in admins:
        all_admins[a.id] = {}
        all_admins[a.id]["user_id"] = a.user_id
        all_admins[a.id]["storage"] = a.storagesize
        all_admins[a.id]["perm"] = a.permlevel
    return render_template('users.html', admins=all_admins)

@admin.route('/admin/remove/<db_id>')
@requires_authorization
def remove_admin(db_id):
    user = discord.fetch_user()
    if not isAdmin(user): return redirect(url_for('index'))
    if not checkPerms(user): return redirect(url_for('index'))
    admin = Admins.query.get(db_id)
    admin.delete()
    return redirect(url_for('admin.admin_users'))

@admin.route('/admin/add', methods=['GET', 'POST'])
@requires_authorization
def add_admin():
    user = discord.fetch_user()
    if not isAdmin(user): return redirect(url_for('index'))
    if not checkPerms(user): return redirect(url_for('index'))
    form = AddAdmin()
    if request.method == 'POST':
        if form.validate():
            user_id = form.user_id.data
            maximg = form.maximages.data
            permlvl = form.permlevel.data
            if not user_id: return flash('No User ID was provided')
            check = Admins.query.filter(Admins.user_id.in_([user_id])).all()
            if check: return flash('That user is already an admin')
            auth_key = generateAuthKey()
            if int(permlvl) != 0: permlvl = 1
            admin = Admins(user_id, user_id, maximg, auth_key, permlvl)
            admin.save()
            return redirect(url_for('admin.admin_users'))
    form.maximages.data = 100
    form.permlevel.data = 0
    return render_template('add.html', form=form)
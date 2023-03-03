from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField

class ChangeSettings(FlaskForm):
    name = StringField('name')
    description = TextAreaField('description')
    webhook = StringField('webhook')
    submit = SubmitField()
    
class AddAdmin(FlaskForm):
    user_id = StringField('id')
    maximages = IntegerField('max')
    permlevel = IntegerField('perm')
    submit = SubmitField()
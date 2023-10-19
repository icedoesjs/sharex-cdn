from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired

class UploadFile(FlaskForm):
    file = FileField(validators=[FileRequired(message="Please provide a file to upload.")])
    submit = SubmitField()
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, FloatField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Optional
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

class OrganisationForm(FlaskForm):
    organisation_name=StringField('Organisation Name',validators=[DataRequired()])
    organisation_address=StringField('Organisation Address',validators=[DataRequired()])
    organisation_phone=StringField('Organisation Phone')
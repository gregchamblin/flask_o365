from flask_wtf import FlaskForm
from wtforms import FileField, HiddenField, SelectField, StringField, SubmitField, TextAreaField#, DateField, TimeField
from wtforms.validators import DataRequired
import wtforms.fields.html5 as html5

brands = SelectField("Store Brand", validators=[DataRequired()], choices=[('VSS','VSS'),('BBW','BBW')])
numbers = StringField("Store Number", validators=[DataRequired()])

class SearchForm(FlaskForm):
    storebrand = brands
    storenumber = numbers
    constphase = SelectField("Construction Phase", validators=[DataRequired()], choices=[('Temp/Wire','Temp/Wire'),('Temp/Box Confirmation','Temp/Box Confirmation'),
        ('Temp/Install','Temp/Install'),('Temp/De-Install','Temp/De-Install'),('Temp/Revisit','Temp/Revisit'),('Perm/CCV','Perm/CCV'),('Perm/Pre-Wire','Perm/Pre-Wire'),('Perm/Wire','Perm/Wire'),
        ('Perm/Install','Perm/Install'),('Perm/De-Install','Perm/De-Install'),('Perm/Revisit','Perm/Revisit')])
    search = SubmitField("Search")

class UploadForm(FlaskForm):
    count = HiddenField()
    imagetype = HiddenField()
    image = FileField(validators=[DataRequired()])
    upload = SubmitField("Upload")

class CheckInOutForm(FlaskForm):
    techonename = StringField("Tech One Name", validators=[DataRequired()])
    techtwoname = StringField("Tech Two Name")
    storebrand = brands
    storenumber = numbers
    datefield = html5.DateField("Date of Arrival", validators=[DataRequired()])
    timefield = html5.TimeField("Time of Arrival")
    activitytype = SelectField("Activity", validators=[DataRequired()], choices=[('Check-In','Check-In'),('Check-Out','Check-Out')])
    notes = TextAreaField("Notes")
    submit = SubmitField("Submit")

class IssuesForm(FlaskForm):
    storebrand = brands
    storenumber = numbers
    devaffected = StringField("Device Affected", validators=[DataRequired()])
    issuedesc = StringField("Description of issue", validators=[DataRequired()])
    tech = StringField("Tech Name", validators=[DataRequired()])
    image = FileField(validators=[DataRequired()])
    upload = SubmitField("Upload")
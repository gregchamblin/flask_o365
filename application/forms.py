from flask_wtf import FlaskForm
from wtforms import FileField, HiddenField, SelectField, StringField, SubmitField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired
import json
# import wtforms.fields.html5 as html5

def fieldlist (fieldtype, key1, key2):
    jsondata = json.load(open('files.json'))
    brands = jsondata[fieldtype]
    brandlistdata = []
    for each in brands:
        data = (each[key1], each[key2])
        brandlistdata.append(data)
    return brandlistdata

brand_list = fieldlist("Brands", "brand", "subbrand")
constphase_list = fieldlist("Phases", "constphase", "constphase")

brands = SelectField("Store Brand", validators=[DataRequired()], choices=brand_list)
numbers = StringField("Store Number", validators=[DataRequired()])

class SearchForm(FlaskForm):
    storebrand = brands
    storenumber = numbers
    constphase = SelectField("Construction Phase", validators=[DataRequired()], choices=constphase_list)
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
    datefield = DateField("Date of Arrival", validators=[DataRequired()])
    timefield = TimeField("Time of Arrival", validators=[DataRequired()])
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

class AdminForm(FlaskForm):
    submit = SubmitField("Submit")
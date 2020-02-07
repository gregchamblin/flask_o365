from application import app
from flask import Flask, request, render_template, redirect, json, Response, url_for, session
from application.forms import SearchForm, UploadForm, IssuesForm, CheckInOutForm
import requests
from fileaccess import file_names, file_upload, list_tech_docs, incident_upload, checkinout

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/docs")
def  docs():
    doclist = list_tech_docs()
    return render_template("docs.html", data={"doclist":doclist})

@app.route("/search", methods=["GET","POST"])
def search():
    session.clear()
    searchform = SearchForm(meta={"csrf": False})
    if searchform.validate_on_submit():
        return redirect("/deliverables")
    return render_template("search.html", form=searchform)

@app.route("/deliverables", methods=["GET","POST"])
def deliverables():
    if 'storebrand' not in session:
        session['storebrand'] = request.form.get('storebrand')
    if 'storenumber' not in session:
        session['storenumber'] = "{:05d}".format(int(request.form.get('storenumber')))
    if 'constphase' not in session:
        session['constphase'] = request.form.get('constphase')

    uploadform = UploadForm(meta={"csrf": False})

    try:
        typedetails = file_names(session['storebrand'], session['storenumber'], session['constphase'])
    except Exception as e:
        return render_template("errors.html", data={"error":str(e)})

    if uploadform.validate_on_submit():
        f = uploadform.image.data
        numfiles = int(request.form.get('count'))
        imagetype = request.form.get('imagetype')
        file_upload(session['storebrand'], session['storenumber'], session['constphase'], numfiles, imagetype, f)
        return redirect("/deliverables")
    return render_template("deliverables.html", data={"storebrand":session['storebrand'], "storenumber":session['storenumber'], "constphase":session['constphase'], "typedetails":typedetails}, form=uploadform)

@app.route("/checkinout", methods=["GET","POST"])
def checkinoutpage():
    checkinoutform = CheckInOutForm(meta={"csrf": False})
    if checkinoutform.validate_on_submit():
        storebrand = request.form.get('storebrand')
        storenumber = "{:05d}".format(int(request.form.get('storenumber')))
        techonename = request.form.get('techonename')
        techtwoname = request.form.get('techtwoname')
        date = request.form.get('datefield')
        time = request.form.get('timefield')
        activitytype = request.form.get('activitytype')
        notes = request.form.get('notes')

        params = {"fields":{"Title": techonename, "Store": storebrand + storenumber, "TechAssistantName": techtwoname, "Activity": activitytype, "Notes": notes, "Date": date, "Time": time}}

        try:
            checkinout(params)
        except Exception as e:
            return render_template("errors.html", data={"error":str(e)})
        return redirect("/")
    return render_template("checkinout.html", form=checkinoutform)

@app.route("/issues", methods=["GET","POST","PATCH"])
def issues():
    issuesform = IssuesForm(meta={"csrf": False})
    if issuesform.validate_on_submit():
        f = issuesform.image.data
        storebrand = request.form.get('storebrand')
        storenumber = "{:05d}".format(int(request.form.get('storenumber')))
        devaffected = request.form.get('devaffected')
        issuedesc = request.form.get('issuedesc')
        tech = request.form.get('tech')
        try:
            incident_upload(storebrand, storenumber, f, devaffected, issuedesc, tech)
        except Exception as e:
            return render_template("errors.html", data={"error":str(e)})
        return redirect("/")
    return render_template("issues.html", form=issuesform)



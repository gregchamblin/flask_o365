import json
import requests
from requests.api import put
import datetime as dt

def get_auth():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': 'd55ca07c-83f0-427d-8636-160561227560',
        'client_secret': 'y10xdC8ql1oLTbgYqxLoEQoHF@ZQV]:-',
        'host': 'https://login.microsoftonline.com',
        'scope': 'https://graph.microsoft.com/.default'
        }
    r = requests.post('https://login.microsoftonline.com/f3860fd5-bb86-4203-9371-f513de7ad3ae/oauth2/v2.0/token', data=payload)
    response = json.loads(r.text)

    token_info = {
        'Authorization': response['token_type'] + ' ' + response['access_token'],
        'Host': 'graph.microsoft.com'
    }

    return token_info

def file_names(brand, storenum, phase):
    base_url = 'https://graph.microsoft.com/beta/drives/b!p92mbUg5S0KkVBsb2JqAsgN3P6jNjl5LvIzDB2nmy1GcjG1J5YVbS4v6mN-7xeO3/root:/General/Deliverables/'
    token_info = get_auth()
    jsondata = json.load(open('files.json'))
    values = jsondata['Value']
    filelist = []

    response = requests.get(base_url + brand + storenum + '/' + phase + ':/children?select=name', headers=token_info)

    if response.status_code != 200:
        raise Exception("Brand, store number or phase does not exist.")
    
    content = response.json()
    filedets = content['value']
    for each in filedets:
        for key in each:
            if key == 'name':
                filelist.append(each[key])
    for each in values:
        if each['constphase'] == phase:
            for file in filelist:
                for details in each['typeinfo']:
                    if details['hwtype'] in file:
                        details['filecount'] = int(details['filecount']) + 1
    return values

def file_upload(brand, storenum, phase, numfiles, imagetype, image):
    token_info = get_auth()
    base_url = 'https://graph.microsoft.com/beta/drives/b!p92mbUg5S0KkVBsb2JqAsgN3P6jNjl5LvIzDB2nmy1GcjG1J5YVbS4v6mN-7xeO3/root:/General/Deliverables/'
    numfiles += 1
    filename = brand + " " + str(int(storenum)) + " " + imagetype + " " + str(numfiles) + ".jpg"
    requests.put(base_url + brand + storenum + '/' + phase + '/' + filename + ":/content", headers=token_info, data=image)

def list_tech_docs():
    token_info = get_auth()

    doclist = []
    content = json.loads(requests.get('https://graph.microsoft.com/beta/drives/b!p92mbUg5S0KkVBsb2JqAsgN3P6jNjl5LvIzDB2nmy1GcjG1J5YVbS4v6mN-7xeO3/root:/General/Docs for Tech:/children', headers=token_info).text)
    values = content['value']
    for each in values:
        mod = dt.datetime.strptime(each['lastModifiedDateTime'][:10], "%Y-%m-%d").date() - dt.date.today()
        mod = int(str(mod).split(" ")[0])
        doclist.append({"link":each['@microsoft.graph.downloadUrl'],"filename":each['name'], "modified":mod})

    return doclist

def incident_upload(brand, storenum, image, devaffected, issuedesc, tech):
    token_info = get_auth()
    url = 'https://graph.microsoft.com/beta/drives/b!p92mbUg5S0KkVBsb2JqAsgN3P6jNjl5LvIzDB2nmy1EQj66RU1e7S4bPqhs5tLlY/'
    response = requests.get(url + 'list/items?$expand=fields', headers=token_info)

    ticketnumber = 0
    content = response.json()
    filedets = content['value']
    for each in filedets:
        fieldsdict = each['fields']
        if int(fieldsdict['LinkFilename'][:9]) >= ticketnumber:
            ticketnumber = int(fieldsdict['LinkFilename'][:9]) + 1

    filename = str(ticketnumber) + ".jpg"
    uploadimage = requests.put(url + 'root:/' + filename + ":/content", headers=token_info, data=image)
    
    detsdict = {'Store': brand + storenum, 'DeviceAffected': devaffected, 'Descriptionofissue': issuedesc, 'TechName': tech, 'TicketNumber': ticketnumber}

    response = requests.get(url + 'list/items?$expand=fields', headers=token_info)
    content = response.json()
    filedets = content['value']
    for each in filedets:
        fieldsdict = each['fields']
        if fieldsdict['LinkFilename'] == str(ticketnumber) + '.jpg':
            itemid = fieldsdict['id']

    patch = requests.patch(url + 'list/items/' + itemid + '/fields', json=detsdict, headers=token_info)

    if patch.status_code != 200:
        raise Exception(patch.json())

def checkinout(params):
    token_info = get_auth()
    url = 'https://graph.microsoft.com/beta/sites/6da6dda7-3948-424b-a454-1b1bd89a80b2/lists/a9ad53a2-a764-47db-a911-82e9d014824d/'

    itempost = requests.post(url + 'items', json=params, headers=token_info)

    if itempost.status_code != 201:
        raise Exception(itempost.json())


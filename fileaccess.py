import json
import requests
from requests.api import put
import datetime as dt
from Private import private

def file_names(brand, storenum, phase):
    base_url = private.return_urls('deliverables_onedrive')
    token_info = private.get_auth()
    jsondata = json.load(open('files.json'))
    values = jsondata['Phases']
    filelist = []

    response = requests.get(base_url + '/' + brand + storenum + '/' + phase + ':/children?select=name', headers=token_info)

    if response.status_code != 200:
        raise Exception("Brand, store number or phase does not exist.")
    
    content = response.json()
    filedets = content['Phases']
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
    token_info = private.get_auth()
    base_url = private.return_urls('deliverables_onedrive')
    numfiles += 1
    filename = brand + " " + str(int(storenum)) + " " + imagetype + " " + str(numfiles) + ".jpg"
    requests.put(base_url + '/' + brand + storenum + '/' + phase + '/' + filename + ":/content", headers=token_info, data=image)

def list_tech_docs():
    token_info = private.get_auth()

    doclist = []
    content = json.loads(requests.get(private.return_urls('docs_onedrive') + ':/children', headers=token_info).text)
    values = content['Phases']
    for each in values:
        mod = dt.datetime.strptime(each['lastModifiedDateTime'][:10], "%Y-%m-%d").date() - dt.date.today()
        mod = int(str(mod).split(" ")[0])
        doclist.append({"link":each['@microsoft.graph.downloadUrl'],"filename":each['name'], "modified":mod})

    return doclist

def incident_upload(brand, storenum, image, devaffected, issuedesc, tech):
    token_info = private.get_auth()
    url = private.return_urls('incident_list')
    response = requests.get(url + '/list/items?$expand=fields', headers=token_info)

    ticketnumber = 0
    content = response.json()
    filedets = content['Phases']
    for each in filedets:
        fieldsdict = each['fields']
        if int(fieldsdict['LinkFilename'][:9]) >= ticketnumber:
            ticketnumber = int(fieldsdict['LinkFilename'][:9]) + 1

    filename = str(ticketnumber) + ".jpg"
    uploadimage = requests.put(url + '/root:/' + filename + ":/content", headers=token_info, data=image)
    
    detsdict = {'Store': brand + storenum, 'DeviceAffected': devaffected, 'Descriptionofissue': issuedesc, 'TechName': tech, 'TicketNumber': ticketnumber}

    response = requests.get(url + '/list/items?$expand=fields', headers=token_info)
    content = response.json()
    filedets = content['Phases']
    for each in filedets:
        fieldsdict = each['fields']
        if fieldsdict['LinkFilename'] == str(ticketnumber) + '.jpg':
            itemid = fieldsdict['id']

    patch = requests.patch(url + '/list/items/' + itemid + '/fields', json=detsdict, headers=token_info)

    if patch.status_code != 200:
        raise Exception(patch.json())

def checkinout(params):
    token_info = private.get_auth()
    url = private.return_urls('checkinout_list')

    itempost = requests.post(url + '/items', json=params, headers=token_info)

    if itempost.status_code != 201:
        raise Exception(itempost.json())


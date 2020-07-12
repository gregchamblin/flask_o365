# flask_o365
    This project utilizes Flask, a web framework for python, and Microsoft Graph API to collect files from individuals working remotely on clients sites and are reporting to a help desk or project team.

Create files.json in root directory of the project.
    Structure should be as follows:

        '''
        {
            "Brands" : [
                {
                    "brand" : "value",
                    "subbrand" : "value"
                }
            ],
            "Phases" : [
                {    
                    "constphase": "phase name or number",
                    "typeinfo": [
                        {
                            "hwtype" : "short type for file name",
                            "hwlabel" : "Descriptive label for website",
                            "hwdescription" : "long description detailing expectation for image contents",
                            "filecount" : "0"
                        }
                    ]
                }
            ]
        }
        '''

Create a directory called "Private".
    create private.py with the following structure

        '''
            import json
            import requests

            def get_auth():
                payload = {
                    'grant_type': 'client_credentials',
                    'client_id': 'XXXXXXXXX',
                    'client_secret': 'XXXXXXXXX',
                    'host': 'https://login.microsoftonline.com',
                    'scope': 'https://graph.microsoft.com/.default'
                    }
                r = requests.post('https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token', data=payload)
                response = json.loads(r.text)

                token = {
                    'Authorization': response['token_type'] + ' ' + response['access_token'],
                    'Host': 'graph.microsoft.com'
                }

                return token

            def return_urls(requestedurl):
                urls = {
                    'deliverables_onedrive' : 'https://graph.microsoft.com/beta/drives/{drive_id}/root:/General/Deliverables',
                    'docs_onedrive' : 'https://graph.microsoft.com/beta/drives/{drive_id}/root:/General/Docs for Tech',
                    'incident_list' : 'https://graph.microsoft.com/beta/drives/{drive_id}',
                    'checkinout_list' : 'https://graph.microsoft.com/beta/sites/{site_id}/lists/{list_id}'
                }
                url = urls[requestedurl]
                return url

        '''
    
    Links for instructions to retreive info above:
        https://docs.microsoft.com/en-us/graph/auth-register-app-v2
            client_secret

        https://docs.microsoft.com/en-us/graph/auth-v2-service#4-get-an-access-token
            client_id
            tenant

        https://docs.microsoft.com/en-us/graph/api/drive-get?view=graph-rest-1.0&tabs=http
            drive_id

        https://docs.microsoft.com/en-us/graph/api/site-get?view=graph-rest-1.0&tabs=http
            site_id

        https://docs.microsoft.com/en-us/graph/api/list-list?view=graph-rest-1.0&tabs=http
            list_id

Create .env file in root diretory.
    '''
    SECRETKEY = SomeSecretkeyforflaskapp
    '''
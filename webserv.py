import requests, json, os, configparser

config = configparser.ConfigParser()
config.read('ils.ini')

#PROD 
ws_server = config['ILS']['server']

def GetToken():
    authData = {'login':config['ILS']['user'], 'password':config['ILS']['pass']}
    authHeadres = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'sd-originating-app-id': 'cs',
                   'x-sirs-clientID': config['ILS']['client']}
    tempTok = requests.post(ws_server + '/user/staff/login', headers=authHeadres, data=json.dumps(authData))
    tempTok = tempTok.json()
    genericHeader = {'Accept': 'application/json',
                     'Content-Type': 'application/json',
                     'sd-originating-app-id': 'cs',
                     'x-sirs-clientID': config['ILS']['client'],
                     'x-sirs-sessionToken': tempTok['sessionToken'],
                     'SD-Working-LibraryID': config['ILS']['library']}
    return {"TOKEN":tempTok['sessionToken'], "HEADER": genericHeader}

def messages(patron):
   result = {'message':'Null', 'status':'Error'}
   if 'messageList' in patron:
       code = patron['messageList'][0]['code']
       if code == 'recordNotFound':
           result['message'] = 'No record found for Library Card'
       else:
           result['message'] = 'Unknown Error : ' + code
   elif patron == '':
           result['message'] = 'No library card number entered'
   else:
       okayProfiles = ['GENERAL','KPLTEACHER','NOFINE','TEACHER']
       if okayProfiles.count(patron['fields']['profile']['key']):
            result['message'] = "PC is now unfiltered"
            result['status'] = 'OK'
       else: 
            result['message'] = 'Library Card not an approved profile'
   return result

def CallAPI(url, payload=None):
    result = ''
    url = ws_server + url

    r = requests.get(url, headers=TOKEN["HEADER"], params=payload)

    try:
        result = r.json()
    except:
        result = ''

    return result

TOKEN = GetToken()

def cardVerify(cardNumber):
   patron = CallAPI('/user/patron/barcode/' + cardNumber, {'includeFields':'profile'})
   return messages(patron)
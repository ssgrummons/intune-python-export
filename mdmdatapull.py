import json
import adal
import requests
import uuid
import logging
import datetime
import time
import wget
import os
from zipfile import ZipFile
#import sqlalchemy

# Configuration file
import config


CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
TENANT_ID = config.TENANT_ID
#RESOURCE = config.RESOURCE
AUTHORITY_URL = 'https://login.microsoftonline.com/' + TENANT_ID

#################################################################################################
#################################################################################################
#                                                                                               #
#                                        Functions                                              #
#                                                                                               #
#################################################################################################
#################################################################################################

def turn_on_logging():
    logging.basicConfig(level=logging.DEBUG)

def getToken(resource):
    context = adal.AuthenticationContext(AUTHORITY_URL, validate_authority=None)
    token = context.acquire_token_with_client_credentials(
        resource,
        CLIENT_ID,
        CLIENT_SECRET)
    return token

def validateToken(token):
    expirationDateObject = datetime.datetime.strptime(token['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
    if expirationDateObject < datetime.datetime.now():
        token = getToken(token['resource'])
    return token

def getGraphData(graph_resource,token):
    try:
        token = validateToken(token)
        http_headers = {'Authorization': f"Bearer {token['accessToken']}",
                                'client-request-id': str(uuid.uuid4())     
                                }
        graphResponse = requests.get(graph_resource, headers=http_headers).json()
        return graphResponse
    except AssertionError as error:
        print(error)

def postGraphData(graph_resource,content,token):
    try:
        token = validateToken(token)
        http_headers = {'Authorization': f"Bearer {token['accessToken']}",
                                'Content-type': 'application/json',
                                'client-request-id': str(uuid.uuid4())     
                                }
        graphResponse = requests.post(graph_resource, headers=http_headers, data=content)
        try:
            return graphResponse.json()
        except:
            return graphResponse
    except AssertionError as error:
        print(error)

def patchGraphData(graph_resource,content,token):
    try:
        token = validateToken(token)
        http_headers = {'Authorization': f"Bearer {token['accessToken']}",
                                'Content-type': 'application/json',
                                'client-request-id': str(uuid.uuid4())     
                                }
        graphResponse = requests.patch(graph_resource, headers=http_headers, data=content)
        return graphResponse
    except AssertionError as error:
        print(error)

def deleteGraphData(graph_resource,token):
    try:
        token = validateToken(token)
        http_headers = {'Authorization': f"Bearer {token['accessToken']}",
                                'client-request-id': str(uuid.uuid4())     
                                }
        graphResponse = requests.delete(graph_resource, headers=http_headers)
        return graphResponse
    except AssertionError as error:
        print(error)

'''
def createExportJob(token):
    try:
        print(currentTimeStr() + ' - Creating an export job request...')
        uri = config.RESOURCE + config.version + config.api
        content = json.dumps(config.report_template)
        response = postGraphData(uri, content, token)
        print(currentTimeStr() + ' - Export job requested')
        return response
    except AssertionError as error:
        print(currentTimeStr() + ' - Error: ' + error)


def checkExportJob(response, token):
    try:
        print(currentTimeStr() + ' - Checking on status of export job...')
        report_id = '/' + response['id']
        uri = config.RESOURCE + config.version + config.api + report_id
        counter = 0
        # Use Counter to enforce a 3 minute time out
        while (response['status'] != 'completed') and (counter <= 36):
            response = getGraphData(uri, token)
            print(currentTimeStr() + ' - Export job status is ' + response['status'])
            if response['status'] != 'completed':
                counter = counter + 1
                time.sleep(5)
        print(currentTimeStr() + ' - Export job complete - Report ready to download')
        return response
    except AssertionError as error:
        print(currentTimeStr() + ' - Error: ' + error)
'''

def dateKeyList(tableSchema):
    datekeys = []
    for item in tableSchema:
        if tableSchema[item] == 'DATETIME':
            datekeys.append(item)
    return datekeys

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    elif s == None:
        return False
    else:
        return s

def currentTimeStr():
    runTime = datetime.datetime.now() 
    timestr = runTime.strftime('%Y-%m-%d %H:%M:%S')
    return timestr

def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("Invalid json: %s" % error)
        return False

def postNewRelicAPI(content):
    try:
        uri = config.nr_resource + config.nr_account + config.nr_api 
        if isinstance(content,dict):
            content = json.dumps(content)
        elif isinstance(content,str):
            if json_validator(content):
                content = content
            else:
                response = {'success': False, 'error': 'incorrect content format'}
                return None
        http_headers = {'X-Insert-Key': config.nr_apikey,
                                'Content-type': 'application/json'
                                }
        response = requests.post(uri, headers=http_headers, data=content).json()
        return response
    except AssertionError as error:
        print(currentTimeStr() + ' - Error: ' + error)


def reverse(lst): 
    new_lst = lst[::-1] 
    return new_lst 

def validateDir(path):
    try:
        path = os.path.normcase(path)
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        if os.path.isdir(abs_path):
            return abs_path
        else:
            print(currentTimeStr() + ' - Path ' + path + " is not a directory")
            print(currentTimeStr() + ' - Exiting program with error')
            # Need better error handling here
    except AssertionError as error:
        print(currentTimeStr() + ' - Error: ' + error)

def saveReport(response, path):
    try:
        path = validateDir(path)
        file_name = reverse((response['url'].split('?')[0]).split('/'))[0]
        file_path = os.path.join(path, file_name)
        print(currentTimeStr() + ' - Writing ' + file_name + ' to disk')
        #report = requests.get(response['url'])
        #open(file_name, 'wb').write(report.content)
        report = wget.download(response['url'], out=file_path)
        print(currentTimeStr() + ' - File ' + file_name + ' written to disk')
        return report
    except AssertionError as error:
        print(currentTimeStr() + ' - Error: ' + error)

def unZipReport(path):
    try:
        # Create a ZipFile Object and load sample.zip in it
        print(currentTimeStr() + ' - Extracting csv report from downloaded zip file')
        with ZipFile(path, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            objectCount = len(zipObj.namelist())
            if objectCount == 1:
                content_name = zipObj.namelist()[0]
                zipObj.extractall(os.path.dirname(path))
                csv_path = os.path.join(os.path.dirname(path), content_name)
        print(currentTimeStr() + ' - CSV report extracted to file ' + str(csv_path))
        os.remove(path)
        print(currentTimeStr() + ' - Zip file deleted')
        return csv_path
    except AssertionError as error:
        print(currentTimeStr() + ' - Error: ' + error)    


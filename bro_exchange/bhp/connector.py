# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 11:41:54 2021

"""

import requests
import requests.auth
import json
import os

# =============================================================================
# Validation
# =============================================================================

def get_base_url(api,demo):
    """
    
    Parameters
    ----------
    api: String
        API version (default = v1)
    demo : Bool
        Defaults to False. If true, the test environment
        of the bronhouderportaal is selected for data exchange
    Returns
    -------
    base_url: String
        base url 

    """    
    if demo == True:
        base_url = 'https://demo.bronhouderportaal-bro.nl'
    elif demo == False:
        base_url = 'https://www.bronhouderportaal-bro.nl'
    if api == 'v1':
        base_url += '/api'
    if api == 'v2':
        base_url += '/api/v2'
    
    return(base_url)

def check_input(token,user,password,project_id,api,demo):
    if token == None:
        if user == None or password == None:
            raise Exception("No user / password supplied for authentication")  
        token = {
            'user':user,
            'pass':password
            }     
    else:
        try:
            if 'user' not in list(token.keys()) and 'password' not in list(token.keys()):
                raise Exception("Supplied token not complete: token should contain the following arguments: 'user', 'password'")  
        except:
            raise Exception("Token invalid: token must be a dict")  

    if api not in ['v1','v2']:
        raise Exception("Selected api not valid")  

    if api == 'v2' and project_id == None:
        raise Exception("A project id must be supplied for using the selected api version")  

    if type(demo) != bool():
        raise Exception("Demo must be a bool")  

def validate_request(payload, token=None, user=None, password= None, api='v1', project_id = None, demo=False):
    """
    

    Parameters
    ----------
    sourcedoc : String
        XML string containing the request.
    token : dictionary
        dictionary with authentication data. keys:
            - user
            - pass
    user:
        Token user. Note: should only be supplied when token isn't generated in advance
    password:
        Token pass. Note: should only be supplied when token isn't generated in advance
    api: String
        API version (default = v1)
    project_id:
        id of the project. Note: required when api > v1
    demo : Bool
        Defaults to False. If true, the test environment
        of the bronhouderportaal is selected for data exchange

    Returns
    -------
    None.

    """
    check_input(token,user,password,project_id,api,demo)

    base_url = get_base_url(api,demo)

    if api == 'v1':
        upload_url = base_url +'/validatie'  
    if api == 'v2':
        upload_url = base_url +'/{project_id}/validatie'  
    
    res = requests.post(upload_url,
        data=payload,
        headers={
            "Content-Type": "application/xml"
        },
        cookies={},
        auth=(token['user'],token['pass']),
    ) 
    
    requestinfo = res.json()
    
    return(requestinfo)


def upload_sourcedocs_from_dict(sourcedocs, token, demo=False):
    """
    

    Parameters
    ----------
    sourcedocs : dictionary
        dictionary containing:
            keys: filenames
            values: XML strings containing the requests.
    token : dictionary
        dictionary with authentication data. keys:
            - user
            - pass
    demo : Bool
        Defaults to False. If true, the test environment
        of the bronhouderportaal is selected for data exchange

    Returns
    -------
    Request response.

    """    
    
    if demo==True:
        base_url = 'https://demo.bronhouderportaal-bro.nl/api'
    else:
        base_url = 'https://www.bronhouderportaal-bro.nl/api'
    
    # Step 1: Create upload
    upload_url = base_url+'/uploads'
    
    try:
        res = requests.post(upload_url,
            headers={
                "Content-Type": "application/xml"
            },
            cookies={},
            auth=(token['user'],token['pass']),
        )         
    except:
        print('Error: unable to create an upload')
        return('Error')
    
    try:
        upload_url_id = res.headers['Location']
    except:
        print('Error: {}'.format(res.text))

    # Step 2: Add source documents to upload
    try:        
        try: 
            
            for sourcedoc in sourcedocs.keys():
                headers = {'Content-type': 'application/xml'}
                params = {'filename':sourcedoc}
                payload = sourcedocs[sourcedoc]
                res = requests.post(upload_url_id+'/brondocumenten',
                    data=payload,
                    headers=headers,
                    cookies={},
                    auth=(token['user'],token['pass']),
                    params = params
                )         
        except:
            print('Error: Cannot add source documents to upload')                   
    
    except:
        print('Error: No source documents found')
        return('Error')
            
        
    # Step 3: Deliver upload
    try:
        upload_id = upload_url_id.split('/')[len(upload_url_id.split('/'))-1]    
        delivery_url = base_url+'/leveringen'
        payload = {'upload':int(upload_id)}
        headers = {'Content-type': 'application/json'}
        endresponse = requests.post(delivery_url,
            data=json.dumps(payload),
            headers=headers,
            cookies={},
            auth=(token['user'],token['pass']),
        )  
        delivery_url_id = endresponse.headers['Location']
        delivery = requests.get(url=delivery_url_id,
            auth=(token['user'],token['pass']),
        ) 
    except:
        print('Error: failed to deliver upload')
        return('Error')

    
    return(delivery)


def upload_sourcedocs_from_dir(input_folder, token, specific_file = None,demo=False):
    """
    
    Parameters
    ----------
    input_folder : string
        Input folder to load sourcedocuments from
        
    token : json
        Acces token for connecting with bronhouderportal project
               
    specific_file : string, optional
        Filename of an specific sourcedocument in the input folder. If this
        parameter is left empty, all sourcedocuments in the input folder 
        will be loaded

    Returns
    -------
    Json string containing information about the delivery (bronhouderportaal api)

    """

    # Step 1: Create upload
    if demo==True:
        base_url = 'https://demo.bronhouderportaal-bro.nl/api'
    else:
        base_url = 'https://www.bronhouderportaal-bro.nl/api'    
    
    
    upload_url = base_url+'/uploads'
    
    try:
        res = requests.post(upload_url,
            headers={
                "Content-Type": "application/xml"
            },
            cookies={},
            auth=(token['user'],token['pass']),
        )          
    except:
        print('Error: unable to create an upload')
    
    upload_url_id = res.headers['Location']

    # Step 2: Add source documents to upload
    if specific_file == None:
        try:
            source_documents = os.listdir(input_folder) 
            
            try: 
                
                for source_document in source_documents:
                    print(source_document)
                    xmlfile = os.path.join(input_folder,source_document)
                    with open(xmlfile, 'r') as file:
                        payload = file.read()
                    headers = {'Content-type': 'application/xml'}
                    params = {'filename':source_document}
                    res = requests.post(upload_url_id+'/brondocumenten',
                        data=payload,
                        headers=headers,
                        cookies={},
                        auth=(token['user'],token['pass']),
                        params = params
                    )             
            except:
                print('Error: Cannot add source documents to upload')                   
        
        except:
            print('Error: No source documents found')
            
    else:
        
        try:

            xmlfile = os.path.join(input_folder,specific_file)
            print(xmlfile)            
            
            try:
                with open(xmlfile, 'r') as file:
                    payload = file.read()
                    headers = {'Content-type': 'application/xml'}
                    params = {'filename':specific_file}
                    res = requests.post(upload_url_id+'/brondocumenten',
                        data=payload,
                        headers=headers,
                        cookies={},
                        auth=(token['user'],token['pass']),
                        params = params
                    )
            except:
                print('Error: Cannot add source documents to upload')    
        except:
            print('Error: No source documents found')
                        
           
    # Step 3: Deliver upload
    try:
        upload_id = upload_url_id.split('/')[len(upload_url_id.split('/'))-1]    
        delivery_url = base_url+'/leveringen'
        payload = {'upload':int(upload_id)}
        headers = {'Content-type': 'application/json'}
        endresponse = requests.post(delivery_url,
            data=json.dumps(payload),
            headers=headers,
            cookies={},
            auth=(token['user'],token['pass']),
        )  
        delivery_url_id = endresponse.headers['Location']
        delivery = requests.get(url=delivery_url_id,
            auth=(token['user'],token['pass']),
        ) 
    except:
        print('Error: failed to deliver upload')
    
    return(delivery)


def check_delivery_status(identifier, token, demo=False):
    """
    

    Parameters
    ----------
    identifier : string
    token : dictionary
        dictionary with authentication data. keys:
            - user
            - pass
    demo : Bool
        Defaults to False. If true, the test environment
        of the bronhouderportaal is selected for data exchange

    Returns
    -------
    Request response.

    """    
    
    if demo==True:
        base_url = 'https://demo.bronhouderportaal-bro.nl/api'
    else:
        base_url = 'https://www.bronhouderportaal-bro.nl/api'
    
    delivery_url_id = base_url+'/leveringen/{}'.format(identifier)
    delivery = requests.get(url=delivery_url_id,
        auth=(token['user'],token['pass']),
    )     
    return(delivery)
    

def get_sourcedocument(identifier, token, demo=False):
    """
    

    Parameters
    ----------
    identifier : string, sourcedocument id
    token : dictionary
        dictionary with authentication data. keys:
            - user
            - pass
    demo : Bool
        Defaults to False. If true, the test environment
        of the bronhouderportaal is selected for data exchange

    Returns
    -------
    Request response.

    """    
    
    if demo==True:
        base_url = 'https://demo.bronhouderportaal-bro.nl/api'
    else:
        base_url = 'https://www.bronhouderportaal-bro.nl/api'
    
    delivery_url_id = base_url+'/brondocumenten/{}'.format(identifier)
    delivery = requests.get(url=delivery_url_id,
        auth=(token['user'],token['pass']),
    )     
    return(delivery)
     
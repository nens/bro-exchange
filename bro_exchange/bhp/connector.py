"""
Created on Wed Nov  3 11:41:54 2021

"""

import json
import os

import requests
import requests.auth

# =============================================================================
# Validation
# =============================================================================


def get_base_url(api, demo):
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
    if demo is True:
        base_url = "https://acc.bronhouderportaal-bro.nl"
    elif demo is False:
        base_url = "https://www.bronhouderportaal-bro.nl"
    if api == "v1":
        base_url += "/api"
    if api == "v2":
        base_url += "/api/v2"

    return base_url


def check_input(token, user, password, project_id, api, demo):
    if token is None:
        if user is None or password is None:
            raise Exception("No user / password supplied for authentication")
        token = {"user": user, "pass": password}
    else:
        try:
            if "user" not in list(token.keys()) and "password" not in list(
                token.keys()
            ):
                raise Exception(
                    "Supplied token not complete: token should contain the following arguments: 'user', 'password'"
                )
        except:
            raise Exception("Token invalid: token must be a dict")

    if api not in ["v1", "v2"]:
        raise Exception("Selected api not valid")

    if api == "v2" and project_id is None:
        raise Exception(
            "A project id must be supplied for using the selected api version"
        )

    if demo is not True and demo is not False:
        raise Exception("Demo must be a bool")

    return token


def met_projectnummer(bro_info):
    try:
        bro_info["projectnummer"]
        available = True
    except:
        available = False

    return available


def validate_sourcedoc(payload, bro_info, demo=False, api="v1"):
    """


    Parameters
    ----------
    sourcedoc : string
        XML string containing the request.
    token : dictionary
        dictionary with authentication data. keys:
            - user
            - pass
    demo : Bool
        Defaults to False. If true, the test environment
        of the bronhouderportaal is selected for data exchange

    Returns
    -------
    None.

    """
    if api == "v1":
        token = bro_info["token"]
        
        if demo is True:
            upload_url = "https://acc.bronhouderportaal-bro.nl/api/validatie"
        else:
            upload_url = "https://www.bronhouderportaal-bro.nl/api/validatie"

        res = requests.post(
            upload_url,
            data=payload,
            headers={"Content-Type": "application/xml"},
            cookies={},
            auth=(token["user"], token["pass"]),
        )
        try:
            requestinfo = res.json()
        except:
            requestinfo = res

    elif api == "v2":
        token = bro_info["token"]
        if met_projectnummer(bro_info):
            if demo is True:
                upload_url = f'https://acc.bronhouderportaal-bro.nl/api/v2/{bro_info["projectnummer"]}/validatie'
            else:
                upload_url = f'https://www.bronhouderportaal-bro.nl/api/v2/{bro_info["projectnummer"]}/validatie'

        else:
            if demo is True:
                upload_url = "https://acc.bronhouderportaal-bro.nl/api/v2/validatie"
            else:
                upload_url = "https://www.bronhouderportaal-bro.nl/api/v2/validatie"


    
        res = requests.post(
            upload_url,
            data=payload,
            headers={"Content-Type": "application/xml"},
            cookies={},
            auth=(token["user"], token["pass"]),
        )
        try:
            requestinfo = res.json()
        except:
            requestinfo = res
            

    return requestinfo


def validate_request(
    payload, token=None, user=None, password=None, api="v1", project_id=None, demo=False
):
    """


    Parameters
    ----------
    request : String
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
    token = check_input(token, user, password, project_id, api, demo)

    base_url = get_base_url(api, demo)

    if api == "v1":
        upload_url = base_url + "/validatie"
    if api == "v2":
        project_id = str(project_id)
        upload_url = base_url + f"/{project_id}/validatie"

    res = requests.post(
        upload_url,
        data=payload,
        headers={"Content-Type": "application/xml"},
        cookies={},
        auth=(token["user"], token["pass"]),
    )

    requestinfo = res.json()

    return requestinfo


def deliver_requests(
    reqs, token=None, user=None, password=None, api="v1", project_id=None, demo=False
):
    """


    Parameters
    ----------
    reqs : dictionary
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
    delivery = None

    token = check_input(token, user, password, project_id, api, demo)

    base_url = get_base_url(api, demo)

    if api == "v1":
        upload_url = base_url + "/uploads"
    if api == "v2":
        project_id = str(project_id)
        upload_url = base_url + f"/{project_id}/uploads"

    try:
        res = requests.post(
            upload_url,
            headers={"Content-Type": "application/xml"},
            cookies={},
            auth=(token["user"], token["pass"]),
        )
    except:
        raise Exception("Error: unable to create an upload")

    try:
        upload_url_id = res.headers["Location"]

        # Step 2: Add source documents to upload
        try:
            for request in reqs.keys():
                headers = {"Content-type": "application/xml"}
                params = {"filename": request}
                payload = reqs[request]
                res = requests.post(
                    upload_url_id + "/brondocumenten",
                    data=payload,
                    headers=headers,
                    cookies={},
                    auth=(token["user"], token["pass"]),
                    params=params,
                )
        except:
            raise Exception("Error: Cannot add source documents to upload")

        # Step 3: Deliver upload
        try:
            upload_id = upload_url_id.split("/")[len(upload_url_id.split("/")) - 1]
            if api == "v1":
                delivery_url = base_url + "/leveringen"
            if api == "v2":
                delivery_url = base_url + f"/{project_id}/leveringen"
            payload = {"upload": int(upload_id)}
            headers = {"Content-type": "application/json"}
        except:
            raise Exception("Error: failed to deliver upload")

        endresponse = requests.post(
            delivery_url,
            data=json.dumps(payload),
            headers=headers,
            cookies={},
            auth=(token["user"], token["pass"]),
        )
        try:
            delivery_url_id = endresponse.headers["Location"]
        except:
            return endresponse

        delivery = requests.get(
            url=delivery_url_id,
            auth=(token["user"], token["pass"]),
        )

        return delivery
    except:
        delivery = res

    return delivery


def upload_sourcedocs_from_dict(
    reqs, token=None, user=None, password=None, api="v1", project_id=None, demo=False
):
    """


    Parameters
    ----------
    reqs : dictionary
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
    delivery = None

    token = check_input(token, user, password, project_id, api, demo)

    base_url = get_base_url(api, demo)

    if api == "v1":
        upload_url = base_url + "/uploads"

    if api == "v2":
        project_id = str(project_id)
        upload_url = base_url + f"/{project_id}/uploads"

    print(upload_url)

    try:
        res = requests.post(
            upload_url,
            headers={"Content-Type": "application/xml"},
            cookies={},
            auth=(token["user"], token["pass"]),
        )
    except:
        print(res.json())
        print("Error: unable to create an upload")
        return "Error"

    try:
        upload_url_id = res.headers["Location"]
    except:
        print(f"Error: {res.text}")

    # Step 2: Add source documents to upload
    try:
        try:
            for request in reqs.keys():
                headers = {"Content-type": "application/xml"}
                params = {"filename": request}
                payload = reqs[request]
                res = requests.post(
                    upload_url_id + "/brondocumenten",
                    data=payload,
                    headers=headers,
                    cookies={},
                    auth=(token["user"], token["pass"]),
                    params=params,
                )
        except:
            print("Error: Cannot add source documents to upload")

    except:
        print("Error: No source documents found")
        return "Error"

    # Step 3: Deliver upload
    try:
        upload_id = upload_url_id.split("/")[len(upload_url_id.split("/")) - 1]
        if api == "v1":
            delivery_url = base_url + "/leveringen"
        if api == "v2":
            delivery_url = base_url + f"/{project_id}/leveringen"
        payload = {"upload": int(upload_id)}
        headers = {"Content-type": "application/json"}
        endresponse = requests.post(
            delivery_url,
            data=json.dumps(payload),
            headers=headers,
            cookies={},
            auth=(token["user"], token["pass"]),
        )
        delivery_url_id = endresponse.headers["Location"]
        delivery = requests.get(
            url=delivery_url_id,
            auth=(token["user"], token["pass"]),
        )
    except:
        print(endresponse.json())
        print("Error: failed to deliver upload")
        return "Error"

    return delivery


def upload_sourcedocs_from_dir(
    input_folder,
    token=None,
    user=None,
    password=None,
    api="v1",
    project_id=None,
    demo=False,
    specific_file=None,
):
    """

    Parameters
    ----------
    input_folder : string
        Input folder to load requestuments from

    token : json
        Acces token for connecting with bronhouderportal project

    specific_file : string, optional
        Filename of an specific requestument in the input folder. If this
        parameter is left empty, all requestuments in the input folder
        will be loaded

    Returns
    -------
    Json string containing information about the delivery (bronhouderportaal api)

    """
    delivery = None

    token = check_input(token, user, password, project_id, api, demo)

    # Step 1: Create upload
    base_url = get_base_url(api, demo)

    if api == "v1":
        upload_url = base_url + "/uploads"
    if api == "v2":
        project_id = str(project_id)
        upload_url = base_url + f"/{project_id}/uploads"

    try:
        res = requests.post(
            upload_url,
            headers={"Content-Type": "application/xml"},
            cookies={},
            auth=(token["user"], token["pass"]),
        )
    except:
        print("Error: unable to create an upload")

    upload_url_id = res.headers["Location"]

    # Step 2: Add source documents to upload
    if specific_file is None:
        try:
            source_documents = os.listdir(input_folder)

            try:
                for source_document in source_documents:
                    xmlfile = os.path.join(input_folder, source_document)
                    with open(xmlfile) as file:
                        payload = file.read()
                    headers = {"Content-type": "application/xml"}
                    params = {"filename": source_document}
                    res = requests.post(
                        upload_url_id + "/brondocumenten",
                        data=payload,
                        headers=headers,
                        cookies={},
                        auth=(token["user"], token["pass"]),
                        params=params,
                    )
            except:
                print("Error: Cannot add source documents to upload")

        except:
            print("Error: No source documents found")

    else:
        try:
            xmlfile = os.path.join(input_folder, specific_file)

            try:
                with open(xmlfile) as file:
                    payload = file.read()
                    headers = {"Content-type": "application/xml"}
                    params = {"filename": specific_file}
                    res = requests.post(
                        upload_url_id + "/brondocumenten",
                        data=payload,
                        headers=headers,
                        cookies={},
                        auth=(token["user"], token["pass"]),
                        params=params,
                    )
            except:
                print("Error: Cannot add source documents to upload")
        except:
            print("Error: No source documents found")

    # Step 3: Deliver upload
    try:
        upload_id = upload_url_id.split("/")[len(upload_url_id.split("/")) - 1]
        if api == "v1":
            delivery_url = base_url + "/leveringen"
        if api == "v2":
            delivery_url = base_url + f"/{project_id}/leveringen"
        payload = {"upload": int(upload_id)}
        headers = {"Content-type": "application/json"}
        endresponse = requests.post(
            delivery_url,
            data=json.dumps(payload),
            headers=headers,
            cookies={},
            auth=(token["user"], token["pass"]),
        )
        delivery_url_id = endresponse.headers["Location"]
        delivery = requests.get(
            url=delivery_url_id,
            auth=(token["user"], token["pass"]),
        )
    except:
        print("Error: failed to deliver upload")

    return delivery


def check_delivery_status(
    identifier,
    token=None,
    user=None,
    password=None,
    api="v1",
    project_id=None,
    demo=False,
):
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
    delivery = None

    token = check_input(token, user, password, project_id, api, demo)

    # Step 1: Create upload
    base_url = get_base_url(api, demo)

    if api == "v1":
        delivery_url_id = base_url + f"/leveringen/{identifier}"
    if api == "v2":
        project_id = str(project_id)
        delivery_url_id = base_url + f"/{project_id}/leveringen/{identifier}"

    delivery = requests.get(
        url=delivery_url_id,
        auth=(token["user"], token["pass"]),
    )
    return delivery


def get_sourcedocument(
    identifier,
    token=None,
    user=None,
    password=None,
    api="v1",
    project_id=None,
    demo=False,
):
    """


    Parameters
    ----------
    identifier : string, requestument id
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
    delivery = None

    token = check_input(token, user, password, project_id, api, demo)

    # Step 1: Create upload
    base_url = get_base_url(api, demo)

    if api == "v1":
        delivery_url_id = base_url + f"/brondocumenten/{identifier}"
    if api == "v2":
        project_id = str(project_id)
        delivery_url_id = base_url + f"/{project_id}/brondocumenten/{identifier}"

    delivery = requests.get(
        url=delivery_url_id,
        auth=(token["user"], token["pass"]),
    )
    return delivery

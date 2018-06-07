"""Code which actually takes care of application API calls or other business logic"""
from yellowant.messageformat import MessageClass, MessageAttachmentsClass, AttachmentFieldsClass ,MessageButtonsClass
from yellowant import YellowAnt
import traceback

#from yellowant_api.views import ACCESS_TOKEN
from yellowant_api.models import Servicenow_model

import requests
import json




# def oauth():
#     global ACCESS_TOKEN
#     url="https://dev36687.service-now.com/oauth_token.do"
#     headers = {
#         "Content-Type" : "application/x-www-form-urlencoded"
#     }
#     body={
#         "grant_type" : "password",
#         "client_id" : "86d1c83b765a130013e8b0e93ff96e8e",
#         "client_secret" : "VMUnhyJ(B]",
#         "username" : "admin",
#         "password" : "FAY5twjw0KQk",
#     }
#     response=requests.post(url=url, headers=headers, data=body)
#     print(type(response))
#     response=response.json()
#     print(type(response))
#     print(response)
#     ACCESS_TOKEN=response["access_token"]
#     #print(requests.post(url=url, auth=('admin', 'FAY5twjw0KQk'), headers=headers, data=json.dumps(body)))



def create_incident(args,user_integration):
    print("Inside create incident")

    print(user_integration.id)
    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token
    url=" https://dev36687.service-now.com/api/now/table/incident"
    #print(ACCESS_TOKEN)
    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }
    body={
        "sys_created_by" : args.get('caller'),
        "short_description" : args.get('short_description'),
        "number" : args.get('incident_number'),
    }

    response = requests.post(url=url, headers=headers,data=json.dumps(body))
    message=MessageClass()
    print(response)
    message.message_text = "Created Incident"
    return message




def delete_incident(args,user_integration):


    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token

    sys_id = args.get('sys_id')

    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }



    url="https://dev36687.service-now.com/api/now/table/incident/" + sys_id

    response=requests.delete(url=url,headers=headers)

    message = MessageClass()
    message.message_text = "Incident Deleted"

    return message


def get_incident(args,user_integration):

    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token
    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }


    sys_id = args.get('sys_id')
    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id

    response=requests.get(url=url,headers=headers)

    print(response.text)
    message = MessageClass()
    message.message_text = "The incident is"

    attachment = MessageAttachmentsClass()

    field1 = AttachmentFieldsClass()
    field1.title = "Incident Name"
    field1.value = response.json()["result"]["number"]
    attachment.attach_field(field1)

    field1 = AttachmentFieldsClass()
    field1.title = "Created by"
    field1.value = response.json()["result"]["sys_created_by"]
    attachment.attach_field(field1)

    field1 = AttachmentFieldsClass()
    field1.title = "Incident State"
    field1.value = response.json()["result"]["incident_state"]
    attachment.attach_field(field1)



    field1 = AttachmentFieldsClass()
    field1.title = "Description"
    field1.value = response.json()["result"]["description"]
    attachment.attach_field(field1)

    field1 = AttachmentFieldsClass()
    field1.title = "Priority"
    field1.value = response.json()["result"]["priority"]
    attachment.attach_field(field1)

    button = MessageButtonsClass()
    button.text = "Modify State"
    button.value = "Modify State"
    button.name = "Modify State"
    button.command = {"service_application": str(user_integration.yellowant_integration_id), "function_name": "modifystate", "data": {"sys_id":sys_id},
                      "inputs":["state"]}
    attachment.attach_button(button)


    button1 = MessageButtonsClass()
    button1.text = "Close Incident"
    button1.value = "Close Incident"
    button1.name = "Close Incident"
    button1.command = {"service_application": str(user_integration.yellowant_integration_id), "function_name": "closeincident", "data": {"sys_id":sys_id},
                       "inputs": ["close_notes","close_code"]}
    attachment.attach_button(button1)

    button2 = MessageButtonsClass()
    button2.text = "Resolve Incident"
    button2.value = "Resolve Incident"
    button2.name = "Resolve Incident"
    button2.command = {"service_application": str(user_integration.yellowant_integration_id), "function_name": "resolveincident", "data": {"sys_id":sys_id},
                       "inputs": ["resolve_notes","close_code"]}
    attachment.attach_button(button2)

    button3 = MessageButtonsClass()
    button3.text = "Change priority"
    button3.value = "Change priority"
    button3.name = "Change priority"
    button3.command = {"service_application": str(user_integration.yellowant_integration_id), "function_name": "changepriority", "data": {"sys_id":sys_id},
                       "inputs": ["priority"]}
    attachment.attach_button(button3)

    message.attach(attachment)

    print(user_integration.id)
    print(user_integration.yellowant_integration_id)
    return message






def states(args,user_integration):

    m = MessageClass()
    data = {'list': []}

    data['list'].append({"State": 1 , "State-name": "New"})
    data['list'].append({"State": 2 , "State-name": "In Progress"})
    data['list'].append({"State": 3 , "State-name": "On Hold"})


    m.data = data
    return m


def show_impact(args,user_integration):
    m = MessageClass()
    data = {'list': []}
    data['list'].append({"Value": 1 , "name": "High"})
    data['list'].append({"Value": 2 , "name": "Medium"})
    data['list'].append({"Value": 3 , "name": "Low"})


    m.data = data
    return m

def change_impact(args,user_integration):
    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token

    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }
    sys_id = args.get('sys_id')
    impact = args.get('impact')
    body = {
            "priority" : impact
            }
    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id
    response=requests.put(url=url,headers=headers,data=json.dumps(body))

    message = MessageClass()
    message.message_text = "Incident impact changed"

    return message





def show_priorities(args,user_integration):
    m = MessageClass()
    data = {'list': []}
    data['list'].append({"Value": 1 , "name": "Critical"})
    data['list'].append({"Value": 2 , "name": "High"})
    data['list'].append({"Value": 3 , "name": "Moderate"})
    data['list'].append({"Value": 4 , "name": "Low"})
    data['list'].append({"Value": 5 , "name": "Planning"})

    m.data = data
    return m


def change_priority(args,user_integration):
    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token

    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }
    sys_id = args.get('sys_id')
    priority = args.get('priority')
    body = {
            "priority" : priority
            }
    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id
    response=requests.put(url=url,headers=headers,data=json.dumps(body))

    message = MessageClass()
    message.message_text = "Incident priority changed"

    return message



def resolve_incident(args,user_integration):
    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token

    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }
    sys_id = args.get('sys_id')
    resolve_notes = args.get('resolve_notes')
    close_code = args.get('close_code')
    body = {
            "close_code":close_code,
            "close_notes":resolve_notes,
            "state":"6",
            "caller_id":sys_id,
            }

    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id
    response=requests.put(url=url,headers=headers,data=json.dumps(body))

    message = MessageClass()
    message.message_text = "Incident Resolved"

    return message

def close_code(args,user_integration):
    m = MessageClass()
    data = {'list': []}

    data['list'].append({"Name": "Solved (Permanently)"})
    data['list'].append({"Name": "Solved (Work Around)"})
    data['list'].append({"Name": "Solved Remotely (Work Around)"})
    data['list'].append({"Name": "Solved Remotely (Permanently)"})
    data['list'].append({"Name": "Not Solved (Not Reproducible)"})
    data['list'].append({"Name": "Not Solved (Too Costly)"})
    data['list'].append({"Name": "Closed/Resolved By Caller"})

    m.data = data
    return m



def close_incident(args,user_integration):
    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token

    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }
    sys_id = args.get('sys_id')
    close_code = args.get('close_code')
    close_notes = args.get('close_notes')
    body = {
            "close_code":close_code,
            "close_notes":close_notes,
            "state":"7",
            "caller_id":sys_id,
            }

    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id
    response=requests.put(url=url,headers=headers,data=json.dumps(body))

    message = MessageClass()
    message.message_text = "Incident Closed"

    return message





def modify_state(args, user_integration):
    print('Inside modify')
    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token

    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }

    sys_id = args.get('sys_id')
    new_state = int(args.get('state'))
    print(sys_id)
    print(new_state)
    print(type(new_state))
    body = {
        "incident_state": new_state,
        "state" : new_state,
        "short_description": "changing again and again",
    }

    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id
    response=requests.put(url=url,headers=headers,data=json.dumps(body))
    print(response)
    message = MessageClass()
    message.message_text = "Incident state changed"

    return message

def modify_incident():
    if (ACCESS_TOKEN==None):
        oauth()
    incidents = get_incidents()

    print(incidents)
    print(type(incidents))
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ ACCESS_TOKEN
    }

    for i in incidents["result"]:
        print(i["sys_id"]+" "+i["number"])


    print('Choose a sys_id')
    sys_id = input()
    url = "https://dev36687.service-now.com/api/now/table/incident/" + sys_id
    body = {
        "impact" : 2,
        "priority" : 2,
        "number" : "INCIDENT01"
    }
    body["impact"]=int(input('Enter new impact'))
    body["priority"] = int(input('Enter new priority'))
    body["number"] = input('Enter new name')

    response=requests.put(url=url,headers=headers,data=json.dumps(body))

    print(response.text)



def get_incidents(args,user_integration):

    access_token_object = Servicenow_model.objects.get(user_integration=user_integration.id)
    access_token = access_token_object.access_token
    url="https://dev36687.service-now.com/api/now/table/incident"
    headers= {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ access_token
    }

    m = MessageClass()

    response = requests.get(url=url,headers=headers)
    response = response.json()
    response = response["result"]
    data = {'list': []}


    for i in response:
        desc= None
        for k,v in i.items():
            if k=="number":
                #data['list'].append({"Instance_name": v,"sys_id"}:)
                incident = v
                print (v)
            if k=="sys_id":
                sys = v
            if k=="short_description":
                desc = v

        if desc == None:
            desc="Short description not available"
        data['list'].append({"Instance_name": incident+" - "+desc,"sys_id": sys})







    m.data = data
    return m



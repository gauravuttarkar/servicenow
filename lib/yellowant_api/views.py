"""
Business logic for different functions used.
"""
import json
import uuid
import requests
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from yellowant import YellowAnt
from yellowant.messageformat import MessageClass, MessageAttachmentsClass, AttachmentFieldsClass ,MessageButtonsClass

from ..yellowant_command_center.command_center import CommandCenter
from django.urls import reverse
from .models import YellowAntRedirectState, UserIntegration ,Servicenow_model,AppRedirectState

from django.views.decorators.csrf import ensure_csrf_cookie

global ACCESS_TOKEN

def service_now_auth(request):
    global ACCESS_TOKEN
    print (request.user.id)
    code = request.GET.get("code")
    state = request.GET.get("state")
    print("Auth Code is ",code)
    print("---------------------------------")
    print("State is ",state)
    print("---------------------------------")
    servicenow_redirect_state = AppRedirectState.objects.get(state=state)
    ut = servicenow_redirect_state.user_integration
    error = request.GET.get('error', None)
    instance_name=servicenow_redirect_state.instance
    #print(error)

    url = "https://"+servicenow_redirect_state.instance+".service-now.com/oauth_token.do"
    data = {
        "client_secret": servicenow_redirect_state.client_secret,
        "code": code,
        "redirect_uri": settings.BASE_URL + "service-now-auth/",
        "client_id": servicenow_redirect_state.client_id,
        "grant_type": "authorization_code",
    }
    # Url to which request is to be sent for SM access_token.
    access_token_response = requests.post(url, data=data)
    print("==============================")
    print(access_token_response.text)
    print("==============================")
    ACCESS_TOKEN=access_token_response.json()['access_token']
    REFRESH_TOKEN=access_token_response.json()['refresh_token']
    expires_in=access_token_response.json()['expires_in']
    print('Inside service now')
    print(ACCESS_TOKEN)


    qut = Servicenow_model.objects.create(user_integration=ut, access_token=ACCESS_TOKEN,
                                          refresh_token=REFRESH_TOKEN,
                                          update_login_flag=True,
                                          instance=instance_name,
                                          expires_in=expires_in
                                          )

    url = settings.SITE_PROTOCOL + f'{servicenow_redirect_state.subdomain}.' + settings.SITE_DOMAIN_URL + \
          settings.BASE_HREF
    return HttpResponseRedirect(url)



def request_yellowant_oauth_code(request):
    subdomain = request.get_host().split('.')[0]
    """Initiate the creation of a new user integration on YA
    YA uses oauth2 as its authorization framework. This method requests for an oauth2 code from
    YA to start creating a
    new user integration for this application on YA.
    """
    # get the user requesting to create a new YA integration
    user = User.objects.get(id=request.user.id)

    # generate a unique ID to identify the user when YA returns an oauth2 code
    state = str(uuid.uuid4())

    # save the relation between user and state so that we can identify the user when YA returns
    # the oauth2 code
    YellowAntRedirectState.objects.create(user=user.id, state=state, subdomain=subdomain)

    return HttpResponseRedirect("{}?state={}&client_id={}&response_type=code&redirect_url={}".format
                               (settings.YA_OAUTH_URL, state, settings.YA_CLIENT_ID,
                                settings.YA_REDIRECT_URL))



def yellowant_oauth_redirect(request):
    """Receive the oauth2 code from YA to generate a new user integration"""

    print('Inside yellowant_oauth_redirect')
    code = request.GET.get("code")

    # the unique string to identify the user for which we will create an integration
    state = request.GET.get("state")

    # fetch user with the help of state
    yellowant_redirect_state = YellowAntRedirectState.objects.get(state=state)
    user = yellowant_redirect_state.user

    # initialize the YA SDK client with your application credentials
    ya_client = YellowAnt(app_key=settings.YA_CLIENT_ID, app_secret=settings.YA_CLIENT_SECRET,
                          access_token=None,
                          redirect_uri=settings.YA_REDIRECT_URL)

    print (settings.YA_REDIRECT_URL)
    # get the access token for a user integration from YA against the code
    access_token_dict = ya_client.get_access_token(code)
    print (access_token_dict)

    access_token = access_token_dict["access_token"]

    # reinitialize the YA SDK client with the user integration access token
    ya_client = YellowAnt(access_token=access_token)

    # get YA user details
    ya_user = ya_client.get_user_profile()

    # create a new user integration for your application
    user_integration = ya_client.create_user_integration()

    webhook_id = str(uuid.uuid4())
    # save the YA user integration details in your database
    user_t = UserIntegration.objects.create(user=user,
                                            yellowant_user_id=ya_user["id"],
                                            yellowant_team_subdomain=ya_user["team"]["domain_name"],
                                            yellowant_integration_id=user_integration
                                            ["user_application"],
                                            yellowant_integration_invoke_name=user_integration
                                            ["user_invoke_name"],
                                            yellowant_integration_token=access_token,
                                            webhook_id=webhook_id)

    url = settings.SITE_PROTOCOL + f'{yellowant_redirect_state.subdomain}.' + settings.SITE_DOMAIN_URL+ \
          settings.BASE_HREF
    return HttpResponseRedirect(url)


@csrf_exempt
def yellowant_api(request):
    """Receive user commands from YA"""
    data = json.loads(request.POST.get("data"))

    # verify whether the request is genuinely from YA with the help of the verification token
    if data["verification_token"] != settings.YA_VERIFICATION_TOKEN:
        return HttpResponseNotAllowed("Insufficient permissions.")

    # check whether the request is a user command, or a webhook subscription notice from YA
    if data["event_type"] == "command":
        # request is a user command

        # retrieve the user integration id to identify the user
        yellowant_integration_id = data.get("application")

        # invoke name of the command being called by the user
        command_name = data.get("function_name")

        # any arguments that might be present as an input for the command
        args = data.get("args")

        # create a YA Message object with the help of the YA SDK
        message = CommandCenter(yellowant_integration_id, command_name, args).parse()

        # return YA Message object back to YA
        return HttpResponse(message)
    elif data["event_type"] == "webhook_subscription":
        # request is a webhook subscription notice
        pass


def api_key(request):
    data = json.loads(request.body)
    #global ACCESS_TOKEN
    subdomain = request.get_host().split(".")[0]
    state = str(uuid.uuid4())
    AppRedirectState.objects.create(user_integration=data["user_integration_id"],
                                    state=state,
                                    instance=data["instance"],
                                    client_id=data["client_id"],
                                    client_secret=data["client_secret"],
                                    subdomain=subdomain)

    url = ('{}?state={}&response_type=code&client_id={}&redirect_uri={}&client_secret={}'.\
    format("https://"+data["instance"]+".service-now.com/oauth_auth.do", state, data['client_id'], settings.BASE_URL+"service-now-auth/", data['client_secret']))
    print(url)
    return HttpResponse(url, status=200)


@csrf_exempt
def webhooks(request,id=None):
    #print(request.post.data)
    # print(type(request))
    # print((request.body))
    try:
        body=json.loads(json.dumps((request.body.decode("utf-8"))))

    # print("Body is")
    # print(body)
    # print(json.loads(body))
        body=json.loads(body)
    except:
        return HttpResponse("Failed", status=404)

    # print(body['sys_id'])
    User = UserIntegration.objects.get(webhook_id=id)
    service_application = str(User.yellowant_integration_id)
    access_token = User.yellowant_integration_token



    #######    STARTING WEB HOOK PART
    webhook_message = MessageClass()
    webhook_message.message_text = "Incident" + " " + body['state']
    attachment = MessageAttachmentsClass()
    field1 = AttachmentFieldsClass()
    field1.title = "Incident Name"
    field1.value = body['number']
    attachment.attach_field(field1)
    webhook_message.attach(attachment)

    attachment = MessageAttachmentsClass()
    field1 = AttachmentFieldsClass()
    field1.title = "Incident Description"
    field1.value = body['description']
    attachment.attach_field(field1)
    webhook_message.attach(attachment)



    # Creating yellowant object
    yellowant_user_integration_object = YellowAnt(access_token=access_token)

    # Sending webhook message to user
    send_message = yellowant_user_integration_object.create_webhook_message(
        requester_application=User.yellowant_integration_id,
        webhook_name="webhook", **webhook_message.get_dict())
    return HttpResponse("OK", status=200)



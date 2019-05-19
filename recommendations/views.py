from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .sms_parser import SmsParser

# Create your views here.
def home(request):
    pass 

@csrf_exempt
def hello(request):
    if request.POST: 
        resp = MessagingResponse()
        mess = request.POST
        parsed = SmsParser.parse(mess['Body'], mess['From'])
        print(parsed)

        resp.message("The Robots are coming! Head for the hills!")
    else: 
        resp = 'this did not work'
    return HttpResponse(str(resp))

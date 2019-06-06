from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .sms_parser import SmsParser
from .action_dispatcher import ActionDispatcher
from .sms_response_generator import SmsResponseGenerator

def home(request):
    return HttpResponse('Hello World') 

@csrf_exempt
def hello(request):
    if request.POST: 
        try:
            action_template = SmsParser.parse(request.POST['Body'], request.POST['From'])
            action_response = ActionDispatcher.dispatch(action_template)
        except Exception as e:
            action_response = {'message': str(e)}
            
        response = SmsResponseGenerator.generate(action_response)
    else: 
        response = 'this did not work'
    return HttpResponse(str(response))




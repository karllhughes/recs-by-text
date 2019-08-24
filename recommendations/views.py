from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .sms_parser import SmsParser
from .action_dispatcher import ActionDispatcher
from .sms_response_generator import SmsResponseGenerator


@csrf_exempt
def sms(request):
    if request.POST:
        try:
            action_template = SmsParser.parse(request.POST['Body'], request.POST['From'], request.session)
            action_response = ActionDispatcher.dispatch(action_template)
        except Exception as e:
            action_response = {'message': str(e)}

        response = SmsResponseGenerator.generate(action_response)
    else:
        response = 'this did not work'
    return HttpResponse(str(response))

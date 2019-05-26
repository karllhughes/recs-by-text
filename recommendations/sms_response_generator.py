from twilio.twiml.messaging_response import MessagingResponse

class SmsResponseGenerator: 
    @classmethod
    def generate(cls, action_response):
        response = MessagingResponse()
        response.message(action_response['message'])
        return response


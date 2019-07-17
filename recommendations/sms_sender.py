from twilio.rest import Client
import os

class SmsSender:

    client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
    
    @classmethod
    def send_to_user(cls, phone, message):
        response = cls.client.messages.create(
            from_=os.environ['TWILIO_PHONE_NUMBER'],
            body=message,
            to=phone
        )
        print(response)
        
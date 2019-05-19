from .actions import ACTIONS

class SmsParser:

    def parse(message, phone):

        if message[:5] == 'I am ':  
            username = message.split(' ')[-1]
            action = ACTIONS['CreateUser']
            response = { 'action': action, 'payload': {'username': username, 'phone': phone} }
        else:
            raise ValueError('Message could not be parsed.')
        
        return response
            




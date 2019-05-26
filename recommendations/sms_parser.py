from .actions_list import ACTIONS_LIST

class SmsParser:

    def parse(message, phone):

        if message[:5].lower() == 'i am ':  
            username = message.split(' ')[-1]
            action = ACTIONS_LIST['create_user']
            response = { 'action': action, 'payload': {'username': username, 'phone': phone} }
        else:
            raise ValueError('Message could not be parsed.')
        
        return response
            




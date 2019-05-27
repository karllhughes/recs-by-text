from .actions_list import ACTIONS_LIST

class SmsParser:

    def parse(message, phone):

        if message[:5].lower() == 'i am ':  
            username = message.split(' ')[-1]
            action = ACTIONS_LIST['create_user']
            response = { 'action': action, 'payload': {'username': username, 'phone': phone} }
        elif message[:10].lower() == 'recommend ' and message[-6:].lower() == ' to me':
            name = message[10:-6]
            response = {'action': ACTIONS_LIST['create_recommendation_for_me'], 'payload': {'name': name, 'phone': phone}}
        else:
            raise ValueError('Message could not be parsed.')
        
        return response
            




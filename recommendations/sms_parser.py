from .actions_list import ACTIONS_LIST

class SmsParser:

    @classmethod
    def parse(cls,message, phone):

        if cls.is_create_new_user(message):  
            username = message.split(' ')[-1]
            action = ACTIONS_LIST['create_user']
            response = { 'action': action, 'payload': {'username': username, 'phone': phone} }
        elif cls.is_recommendation_for_me(message):
            name = message[10:-6]
            response = {'action': ACTIONS_LIST['create_recommendation_for_me'], 'payload': {'name': name, 'phone': phone}}
        elif cls.is_recommendation_for_another_user(message):
            username = message.split(' ')[-1]
            name = ' '.join(message.split(' ')[1:-2])
            response = {'action' : ACTIONS_LIST['create_recommendation_for_another_user'], 'payload' : {'name': name, 'recommender_phone': phone, 'recommendee_username': username}}
        
        else:
            raise ValueError('Message could not be parsed.')
        
        return response
            
    @classmethod
    def is_recommendation_for_another_user(cls,message):
        message_array = message.split(' ')
        last_word = message_array[-1]
        second_to_last_word = message_array[-2]
        first_word = message_array[0]
        return first_word == 'recommend' and second_to_last_word == 'to' and last_word != 'me'

    @classmethod
    def is_recommendation_for_me(cls,message):
        return message[:10].lower() == 'recommend ' and message[-6:].lower() == ' to me'
    
    @classmethod
    def is_create_new_user(cls,message):
        return message[:5].lower() == 'i am '
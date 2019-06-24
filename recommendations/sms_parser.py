from .actions_list import ACTIONS_LIST
from IPython import embed

def exception_returns_false(func):
    def catch_errors(cls, message, session=None):
        try: 
            return func(cls, message, session)
        except Exception as e:
            return False
    
    return catch_errors

class SmsParser:

    @classmethod
    def parse(cls,message, phone, session):

        if cls.is_create_new_user(message):  
            username = message.split(' ')[-1]
            action = ACTIONS_LIST['create_user']
            response = { 'action': action, 'payload': {'username': username, 'phone': phone, 'session': session} }
        elif cls.is_recommendation_for_me(message):
            name = message[10:-6]
            response = {'action': ACTIONS_LIST['create_recommendation_for_me'], 'payload': {'name': name, 'phone': phone, 'session': session}}
        elif cls.is_rec_for_me(message):
            name = message[4:-6]
            response = {'action': ACTIONS_LIST['create_recommendation_for_me'], 'payload': {'name': name, 'phone': phone, 'session': session}}
        elif cls.is_recommendation_for_another_user(message):
            username = message.split(' ')[-1]
            name = ' '.join(message.split(' ')[1:-2])
            response = {'action' : ACTIONS_LIST['create_recommendation_for_another_user'], 'payload' : {'name': name, 'recommender_phone': phone, 'recommendee_username': username, 'session': session} }
        elif cls.is_recommendation_acception(message):
            response = {'action': ACTIONS_LIST['accept_recommendation_from_another_user'], 'payload': {'recommendation_id': message[1:], 'phone': phone, 'session': session}}
        elif cls.is_view_list(message):
            response = {'action': ACTIONS_LIST['view_list'], 'payload': {'phone': phone, 'session': session}}
        elif cls.is_ask_from_another_user(message):
            askee_username = message[4:]
            response = {'action': ACTIONS_LIST['ask_from_another_user'], 'payload': {'asker_phone': phone, 'askee_username': askee_username, 'session': session}}
        elif cls.is_delete(message):
            position_in_list = message[7:]
            response = {'action': ACTIONS_LIST['delete'], 'payload': {'phone': phone, 'position_in_list': position_in_list, 'session': session}}
        elif cls.is_view_single_recommendation(message):
            position_in_list = message[5:]
            response = {'action': ACTIONS_LIST['view_single_recommendation'], 'payload': {'phone': phone, 'position_in_list': position_in_list, 'session': session}}
        elif cls.is_add_context(message, session):
            response = {'action': ACTIONS_LIST['add_context'], 'payload': {'phone': phone, 'session': session, 'context': message}}
        elif cls.is_invite(message):
            invite_number = message[7:]
            response = {'action': ACTIONS_LIST['invite'], 'payload': {'phone': phone, 'context': message, 'invite_number': invite_number}}
        else:
            raise ValueError('Message could not be parsed.')
        
        return response
    
    @classmethod
    @exception_returns_false
    def is_recommendation_for_another_user(cls,message, session):
        message_array = message.split(' ')
        last_word = message_array[-1]
        second_to_last_word = message_array[-2]
        first_word = message_array[0]
        return (first_word.lower() == 'recommend' or first_word.lower() == 'rec') and second_to_last_word.lower() == 'to' and last_word.lower() != 'me'
       
    @classmethod
    @exception_returns_false
    def is_recommendation_for_me(cls,message, session):
        return message[:10].lower() == 'recommend ' and message[-6:].lower() == ' to me'

    @classmethod
    @exception_returns_false
    def is_rec_for_me(cls,message, session):
        return message[:4].lower() == 'rec ' and message[-6:].lower() == ' to me'
        
    @classmethod
    @exception_returns_false
    def is_create_new_user(cls,message, session):
        return message[:5].lower() == 'i am '
        
    
    @classmethod
    @exception_returns_false
    def is_recommendation_acception(cls, message, session):
        return message[0].lower() == 'r' and message[1:].isdigit()

    @classmethod
    @exception_returns_false
    def is_view_list(cls, message, session):
        return message.strip().lower() == 'list'

    @classmethod
    @exception_returns_false
    def is_ask_from_another_user(cls, message, session):
        return message[:4].lower() == 'ask ' 

    @classmethod
    @exception_returns_false
    def is_delete(cls, message, session):
        return message[:7].lower() == 'delete ' 
        
    @classmethod
    @exception_returns_false
    def is_add_context(cls, message, session):
        return bool(session['latest_recommendation_id'])

    @classmethod
    @exception_returns_false
    def is_view_single_recommendation(cls, message, session):
        return message[:5].lower() == 'show '

    @classmethod
    @exception_returns_false
    def is_invite(cls, message, session):
        return message[:7].lower() == 'invite '
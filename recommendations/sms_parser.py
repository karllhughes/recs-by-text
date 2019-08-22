from .actions_list import ACTIONS_LIST
import re


def exception_returns_false(func):
    def catch_errors(cls, message, session=None):
        try: 
            return func(cls, message, session)
        except Exception as e:
            return False
    
    return catch_errors


class SmsParser:

    @classmethod
    def parse(cls, message, phone, session):
        action = cls.get_action_from_message(message)

        if action == ACTIONS_LIST['create_user']:
            response = {'action': action, 'payload': {'username': cls.matches[2], 'phone': phone, 'session': session}}
        elif action == ACTIONS_LIST['create_recommendation_for_me']:
            response = {'action': action, 'payload': {'name': cls.matches[2], 'phone': phone, 'session': session}}
        elif action == ACTIONS_LIST['create_recommendation_for_another_user']:
            response = {'action': action, 'payload': {'name': cls.matches[2], 'recommender_phone': phone, 'recommendee_username': cls.matches[4], 'session': session}}
        elif action == ACTIONS_LIST['accept_recommendation_from_another_user']:
            response = {'action': action, 'payload': {'recommendation_id': cls.matches[1], 'phone': phone, 'session': session}}
        elif action == ACTIONS_LIST['view_list']:
            response = {'action': action, 'payload': {'phone': phone, 'session': session}}
        elif action == ACTIONS_LIST['ask_from_another_user']:
            response = {'action': action, 'payload': {'asker_phone': phone, 'askee_username': cls.matches[2], 'session': session}}
        elif action == ACTIONS_LIST['delete']:
            response = {'action': action, 'payload': {'phone': phone, 'position_in_list': cls.matches[2], 'session': session}}
        elif action == ACTIONS_LIST['view_single_recommendation']:
            response = {'action': action, 'payload': {'phone': phone, 'position_in_list': cls.matches[3], 'session': session}}
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
    def get_action_from_message(cls, message, session):
        patterns = {
            # Create account
            '^(i am|call me) ([a-z0-9_]+)$': ACTIONS_LIST['create_user'],
            # Add to my list
            '^(recommend|rec|add) \\b(.*) (to|for) (me|my list).*$': ACTIONS_LIST['create_recommendation_for_me'],
            # Add to another user's list
            '^(recommend|rec|add) \\b(.*) (to|for) (?!me\\b|my list)\\b([a-z0-9_]+).*$': ACTIONS_LIST['create_recommendation_for_another_user'],
            # Accept recommendation
            '^r([0-9]+)$': ACTIONS_LIST['accept_recommendation_from_another_user'],
            # Show my list
            '^(list|my list)$': ACTIONS_LIST['view_list'],
            # Ask another user for a recommendation
            '^(ask|request|rec from|recommendation from) ([a-z0-9_]+)\\b.*$': ACTIONS_LIST['ask_from_another_user'],
            # Remove from your list
            '^(rm|delete|remove|del) ([0-9]+)\\b.*$': ACTIONS_LIST['delete'],
            # Show a single item from your list
            '^(show?( me)*) ([0-9]+)\\b.*$': ACTIONS_LIST['view_single_recommendation'],
        }

        for pattern, action_name in patterns.items():
            matches = re.match(pattern, message, re.IGNORECASE | re.MULTILINE)
            if matches:
                cls.matches = matches
                return action_name

    @classmethod
    @exception_returns_false
    def is_add_context(cls, message, session):
        return bool(session['latest_recommendation_id'])

    @classmethod
    @exception_returns_false
    def is_invite(cls, message, session):
        return message[:7].lower() == 'invite '
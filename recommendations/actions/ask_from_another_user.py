from recommendations.models import User, TrustedUser
from recommendations.sms_sender import SmsSender
from .base_action import BaseAction


class AskFromAnotherUser(BaseAction):

    @classmethod
    def execute(cls, payload):
        asker = User.objects.get(phone=payload['asker_phone'])
        askee = User.objects.get(username=payload['askee_username'])
        
        if not asker.does_trust(askee):
            TrustedUser.objects.create(original_user=asker, trusted_user=askee)

    
        SmsSender.send_to_user(askee, f"{asker.username} asked for a recommendation. To send one, text 'recommend XXXX to {asker.username}'.")
        super().clear_recommendation_id(payload['session'])

        return {'message': f"'{askee.username}' was asked for a recommendation."}


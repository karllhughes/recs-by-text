from .base_action import BaseAction
from recommendations.sms_sender import SmsSender

class SendInvite(BaseAction):

    @classmethod
    def execute(cls, payload):
        original_user = User.objects.get(phone=payload['phone'])
        recommendation = Recommendation.objects.get(id=payload['recommendation_id'], recommendee=original_user)
        recommendation.accepted = True 
        recommendation.save()
        TrustedUser.objects.create(original_user=original_user, trusted_user=recommendation.recommender)
        super().clear_recommendation_id(payload['session'])
        return {'message': f"'{recommendation.name}' has been added to your list."}

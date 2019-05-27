from recommendations.models import Recommendation, User, TrustedUser
from django.core.exceptions import ObjectDoesNotExist
from recommendations.sms_sender import SmsSender

class CreateRecommendationForAnotherUser: 

    @classmethod
    def execute(cls, payload):
        recommender = User.objects.get(phone=payload['recommender_phone'])
        recommendee = User.objects.get(username=payload['recommendee_username'])
        is_trusted = cls.is_trusted_by(recommender, recommendee)
        recommendation = Recommendation(recommender=recommender, recommendee=recommendee, name=payload['name'], accepted=is_trusted)
        
        recommendation.full_clean()
        recommendation.save()

        if is_trusted: 
            SmsSender.send_to_user(recommendee, f"{recommender.username} recommended '{recommendation.name}' to you.")
        else: 
            pass
        return {'message': f"'{recommendation.name}' was recommended to {recommendee.username}."}

    @classmethod
    def is_trusted_by(cls, recommender, recommendee):
        try: 
            return bool(TrustedUser.objects.get(original_user=recommendee, trusted_user=recommender))
        except ObjectDoesNotExist as e:
            return False

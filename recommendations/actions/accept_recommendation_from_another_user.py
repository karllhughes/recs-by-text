from recommendations.models import Recommendation, User, TrustedUser

class AcceptRecommendationFromAnotherUser:

    @classmethod
    def execute(cls, payload):
        original_user = User.objects.get(phone=payload['phone'])
        recommendation = Recommendation.objects.get(id=payload['recommendation_id'], recommendee=original_user)
        recommendation.accepted = True 
        recommendation.save()
        TrustedUser.objects.create(original_user=original_user, trusted_user=recommendation.recommender)
        return {'message': f"'{recommendation.name}' has been added to your list."}

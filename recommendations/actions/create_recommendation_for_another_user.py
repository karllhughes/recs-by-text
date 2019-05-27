from recommendations.models import Recommendation, User

class CreateRecommendationForAnotherUser: 

    @classmethod
    def execute(cls, payload):
        recommender = User.objects.get(phone=payload['recommender_phone'])
        recommendee = User.objects.get(username=payload['recommendee_username'])
        recommendation = Recommendation(recommender=recommender, recommendee=recommendee, name=payload['name'], accepted=False)
        recommendation.full_clean()
        recommendation.save()
        return {'message': f"'{recommendation.name}' was recommended to {recommendee.username}."}
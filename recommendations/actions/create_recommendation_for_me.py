from recommendations.models import Recommendation, User

class CreateRecommendationForMe: 

    @classmethod
    def execute(cls, payload):
        user = User.objects.get(phone=payload['phone'])
        recommendation = Recommendation(recommender=user, recommendee=user, name=payload['name'], accepted=True)
        recommendation.full_clean()
        recommendation.save()
        return {'message': f"'{recommendation.name}' was added to your list."}
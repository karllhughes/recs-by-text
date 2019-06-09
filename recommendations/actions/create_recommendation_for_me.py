from recommendations.models import Recommendation, User
from .base_action import BaseAction


class CreateRecommendationForMe(BaseAction): 

    @classmethod
    def execute(cls, payload):
        user = User.objects.get(phone=payload['phone'])
        recommendation = Recommendation(recommender=user, recommendee=user, name=payload['name'], accepted=True)
        recommendation.full_clean()
        recommendation.save()
        super().clear_recommendation_id(payload['session'])

        return {'message': f"'{recommendation.name}' was added to your list."}
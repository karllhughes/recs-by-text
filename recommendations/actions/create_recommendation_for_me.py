from recommendations.models import Recommendation, User
from .base_action import BaseAction


class CreateRecommendationForMe(BaseAction): 

    @classmethod
    def execute(cls, payload):
        user = User.objects.get(phone=payload['phone'])
        recommendation = Recommendation(recommender=user, recommendee=user, name=payload['name'], accepted=True)
        recommendation.full_clean()
        recommendation.save()

        cls.set_recommendation_id_in_session(payload['session'], recommendation)

        return {'message': f"'{recommendation.name}' was added to your list. Reply to add context."}

    @classmethod
    def set_recommendation_id_in_session(cls, session, recommendation):
        session['latest_recommendation_id'] = recommendation.id
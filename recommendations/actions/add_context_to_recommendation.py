from recommendations.models import Recommendation
from .base_action import BaseAction


class AddContextToRecommendation(BaseAction):

    @classmethod
    def execute(cls, payload):
        Recommendation.objects.filter(id=payload['session']['latest_recommendation_id']).update(context=payload['context'])
        super().clear_recommendation_id(payload['session'])

        return {'message': f"Context added."}
        
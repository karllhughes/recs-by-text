from recommendations.models import User 
from .base_action import BaseAction


class ViewSingleRecommendation(BaseAction):
    @classmethod
    def execute(cls, payload):
        recommendations = User.objects.get(phone=payload['phone']).recommendations_recieved.filter(accepted=True).order_by('-created_at')
        position = int(payload['position_in_list']) - 1
        recommendation = recommendations[position]
        
        message = f"""
{recommendation.name}
------------------------
CONTEXT: {recommendation.context}
""" 
        super().clear_recommendation_id(payload['session'])
        
        return {'message': message }
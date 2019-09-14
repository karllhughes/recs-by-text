from recommendations.models import User
from .base_action import BaseAction


class ViewList(BaseAction):

    @classmethod
    def execute(cls, payload):
        recommendations = User.objects.get(phone=payload['phone'])\
            .recommendations_recieved\
            .filter(accepted=True)\
            .order_by('-created_at')
        names = ''
        for i, recommendation in enumerate(recommendations):
            names += f'{i + 1}.  {recommendation.name}\n'

        message = f"""
Movies
------------------------
{names}
"""
        super().clear_recommendation_id(payload['session'])
        return {'message': message}

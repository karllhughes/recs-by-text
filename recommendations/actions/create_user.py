from recommendations.models import User
from .base_action import BaseAction


class CreateUserAction(BaseAction):

    @classmethod
    def execute(cls, payload):
        user = User(username=payload['username'], phone=payload['phone'])
        user.full_clean()
        user.save()
        super().clear_recommendation_id(payload['session'])
        return {'message': f"{user.username} created successfully."}

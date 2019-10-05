from recommendations.models import User
from .base_action import BaseAction


class DeleteFromList(BaseAction):

    @classmethod
    def execute(cls, payload):
        recommendations = User.objects.get(phone=payload['phone'])\
            .recommendations_recieved\
            .filter(accepted=True)\
            .order_by('-created_at')
        position = int(payload['position_in_list']) - 1
        rec_to_delete = recommendations[position]
        rec_to_delete.delete()
        super().clear_recommendation_id(payload['session'])

        return {'message': f"'{rec_to_delete.name}' was deleted from your list."}

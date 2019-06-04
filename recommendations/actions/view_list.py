from recommendations.models import User
from recommendations.sms_sender import SmsSender

class ViewList:

    @classmethod 
    def execute(cls, payload):
        recommendations = User.objects.get(phone=payload['phone']).recommendations_recieved.filter(accepted=True)
        names = ''
        for i, recommendation in enumerate(recommendations):
            names += f'{i + 1}.  {recommendation.name}\n'
        
        message = f"""
Movies
------------------------
{names}
"""

        return {'message': message}
        
from recommendations.models import User    

class CreateUserAction: 
    
    @classmethod
    def execute(cls, payload):
        user = User(**payload)
        user.full_clean()
        user.save()
        return {'message': f"{user.username} created successfully."}

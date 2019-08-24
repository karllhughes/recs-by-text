from recommendations.models import Recommendation, User, TrustedUser
from recommendations.sms_sender import SmsSender
from .base_action import BaseAction


class CreateRecommendationForAnotherUser(BaseAction):

    @classmethod
    def execute(cls, payload):
        recommender = User.objects.get(phone=payload['recommender_phone'])
        recommendee = User.objects.get(username=payload['recommendee_username'])
        recommendation = cls.create_recommendation_and_save(recommender, recommendee, payload)
        
        cls.set_recommendation_id_in_session(payload['session'], recommendation)
        cls.send_recommendation_to_recommendee(recommender, recommendee, recommendation)
                 
        return {'message': f"'{recommendation.name}' was recommended to {recommendee.username}. Reply to add context."}

    @classmethod
    def send_recommendation_to_recommendee(cls, recommender, recommendee, recommendation):
        if cls.is_trusted: 
            SmsSender.send_to_user(recommendee.phone, f"{recommender.username} recommended '{recommendation.name}' to you.")
        else: 
            SmsSender.send_to_user(recommendee.phone, f"{recommender.username} recommended '{recommendation.name}' to you. Text back 'r{recommendation.id}' if you would like to add this recommendation and them as a trusted user.")   

    @classmethod
    def create_recommendation_and_save(cls, recommender, recommendee, payload):
        cls.is_trusted = recommender.is_trusted_by(recommendee)
        recommendation = Recommendation(recommender=recommender, recommendee=recommendee, name=payload['name'], accepted=cls.is_trusted)
        recommendation.full_clean()
        recommendation.save()
        return recommendation
   
    @classmethod
    def set_recommendation_id_in_session(cls, session, recommendation):
        session['latest_recommendation_id'] = recommendation.id

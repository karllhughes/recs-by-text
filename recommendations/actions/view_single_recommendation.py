from recommendations.models import User 
from .base_action import BaseAction
from IPython import embed
import urllib.parse
import requests

class ViewSingleRecommendation(BaseAction):
    @classmethod
    def execute(cls, payload):
        recommendations = User.objects.get(phone=payload['phone']).recommendations_recieved.filter(accepted=True).order_by('-created_at')
        position = int(payload['position_in_list']) - 1
        recommendation = recommendations[position]
        url_encoded_rec_name = urllib.parse.quote_plus(recommendation.name)
        rotten_tomatoes = cls.shorten_url(f'https://www.rottentomatoes.com/search/?search={url_encoded_rec_name}')
        imdb_link = cls.shorten_url(f'https://m.imdb.com/find?s=tt&q={url_encoded_rec_name}')
       
        
        message = f"""
{recommendation.name}
------------------------
CONTEXT: {recommendation.context}
IMDB: {imdb_link}
RT: {rotten_tomatoes}
""" 
        super().clear_recommendation_id(payload['session'])
        
        return {'message': message }

    @classmethod
    def shorten_url(cls, original_url):
        try: 
            shrtco_endpoint = f'https://api.shrtco.de/v2/shorten?url={urllib.parse.quote(original_url)}'
            r = requests.post(shrtco_endpoint)
            return r.json()['result']['short_link']
        except Exception as e:
            return original_url
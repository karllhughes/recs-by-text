class BaseAction:

    @classmethod
    def clear_recommendation_id(cls, session):
        if 'latest_recommendation_id' in session.keys():
            del session['latest_recommendation_id']

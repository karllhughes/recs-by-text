from .actions_list import ACTIONS_LIST
from .actions.create_user_action import CreateUserAction
from .actions.create_recommendation_for_me import CreateRecommendationForMe

class ActionDispatcher: 
    @classmethod
    def dispatch(cls,action_template):
        action = action_template['action']
        if action == ACTIONS_LIST['create_user']:
            return CreateUserAction.execute(action_template['payload'])
        elif action == ACTIONS_LIST['create_recommendation_for_me']: 
            return CreateRecommendationForMe.execute(action_template['payload'])
        else: 
            raise ValueError(f"{action_template['action']} is not a valid action.")

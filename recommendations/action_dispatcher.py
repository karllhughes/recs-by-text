from .actions_list import ACTIONS_LIST
from .actions.create_user import CreateUserAction
from .actions.create_recommendation_for_me import CreateRecommendationForMe
from .actions.create_recommendation_for_another_user import CreateRecommendationForAnotherUser
from .actions.accept_recommendation_from_another_user import AcceptRecommendationFromAnotherUser
from .actions.view_list import ViewList
from .actions.ask_from_another_user import AskFromAnotherUser
from .actions.delete_from_list import DeleteFromList
from .actions.add_context_to_recommendation import AddContextToRecommendation
from .actions.view_single_recommendation import ViewSingleRecommendation
from .actions.send_invite import SendInvite


class ActionDispatcher:
    @classmethod
    def dispatch(cls, action_template):
        action = action_template['action']
        if action == ACTIONS_LIST['create_user']:
            return CreateUserAction.execute(action_template['payload'])
        elif action == ACTIONS_LIST['create_recommendation_for_me']:
            return CreateRecommendationForMe.execute(action_template['payload'])
        elif action == ACTIONS_LIST['create_recommendation_for_another_user']:
            return CreateRecommendationForAnotherUser.execute(action_template['payload'])
        elif action == ACTIONS_LIST['accept_recommendation_from_another_user']:
            return AcceptRecommendationFromAnotherUser.execute(action_template['payload'])
        elif action == ACTIONS_LIST['view_list']:
            return ViewList.execute(action_template['payload'])
        elif action == ACTIONS_LIST['ask_from_another_user']:
            return AskFromAnotherUser.execute(action_template['payload'])
        elif action == ACTIONS_LIST['delete']:
            return DeleteFromList.execute(action_template['payload'])
        elif action == ACTIONS_LIST['add_context']:
            return AddContextToRecommendation.execute(action_template['payload'])
        elif action == ACTIONS_LIST['view_single_recommendation']:
            return ViewSingleRecommendation.execute(action_template['payload'])
        elif action == ACTIONS_LIST['invite']:
            return SendInvite.execute(action_template['payload'])
        else:
            raise ValueError(f"{action_template['action']} is not a valid action.")

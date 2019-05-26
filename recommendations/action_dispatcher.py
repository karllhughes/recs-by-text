from .actions_list import ACTIONS_LIST
from .actions.create_user_action import CreateUserAction

class ActionDispatcher: 
    @classmethod
    def dispatch(cls,action_template):
        if action_template['action'] == ACTIONS_LIST['create_user']:
            return CreateUserAction.execute(action_template['payload'])
        else: 
            raise ValueError(f"{action_template['action']} is not a valid action.")

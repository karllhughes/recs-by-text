from .base_action import BaseAction
from recommendations.sms_sender import SmsSender
import phonenumbers


class SendInvite(BaseAction):

    @classmethod
    def execute(cls, payload):
        parsed_number = phonenumbers.parse(payload['invite_number'], 'US')
        number = f"+{parsed_number.country_code}{parsed_number.national_number}"

        if phonenumbers.is_valid_number(parsed_number):
            SmsSender.send_to_user(
                number,
                f"{payload['phone']} sent you an invite to Recs By Text. "
                f"Visit http://recsbytext.com/ for instructions on how to sign up and start making "
                f"recommendations to friends!"
            )
            message = {'message': f"'{number}' was sent an invite to Recs By Text."}
        else:
            message = {'message': f"'{number}' is not a valid phone number."}

        return message

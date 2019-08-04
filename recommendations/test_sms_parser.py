from django.test import TestCase
from recommendations.sms_parser import SmsParser
from .actions_list import ACTIONS_LIST

class AnimalTestCase(TestCase):
    def setUp(self):
        print("Tests are running")

    def test_parse_is_create_new_user_when_username_is_valid(self):
        # Arrange
        message = 'I am Bill'
        phone = '123-456-7890'
        session = {}

        # Act
        result = SmsParser.parse(message, phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_user'])
        self.assertEqual(result['payload']['username'], 'Bill')

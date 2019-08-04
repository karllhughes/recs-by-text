from django.test import TestCase
from unittest import skip
from recommendations.sms_parser import SmsParser
from .actions_list import ACTIONS_LIST
from faker import Faker
import random


class AnimalTestCase(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.phone = self.faker.phone_number()

    def test_parse_is_create_new_user_when_username_is_valid(self):
        # Arrange
        message = 'I am Bill'
        phone = '123-456-7890'
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_user'])
        self.assertEqual(result['payload']['username'], 'Bill')

    def test_parse_is_invite(self):
        invite_number = self.faker.phone_number()
        message = f'invite {invite_number}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['invite'])
        self.assertEqual(result['payload']['invite_number'], invite_number)

    @skip('known issue #50')
    def test_parse_invite_when_invalid_invite_number(self):
        invite_number = '773 555 55'
        message = f'invite {invite_number}'
        session = {}

        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_add_context(self):
        message = ''.join(self.faker.words(5))
        session = {'latest_recommendation_id': random.randint(1,101)}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['add_context'])
        self.assertEqual(result['payload']['context'], message)
        self.assertEqual(result['payload']['session'], session)

    def test_parse_is_view_single_recommendation(self):
        position = str(random.randint(1,15))
        message = f'Show {position}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['view_single_recommendation'])
        self.assertEqual(result['payload']['position_in_list'], position)

    @skip('known issue #51')
    def test_parse_is_view_single_recommendation_when_no_list_position(self):
        message = f'Show '
        session = {}
       
        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_delete(self):
        position = str(random.randint(1,15))
        message = f'Delete {position}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['delete'])
        self.assertEqual(result['payload']['position_in_list'], position)

    def test_parse_ask_from_another_user(self):
        askee_username = self.faker.name()
        message = f'ask {askee_username}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['ask_from_another_user'])
        self.assertEqual(result['payload']['askee_username'], askee_username)

    @skip('known issue')
    def  test_parse_ask_from_another_user_when_no_user_name(self):
        message = f'ask '
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)



        
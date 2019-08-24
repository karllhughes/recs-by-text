from django.test import TestCase
from recommendations.sms_parser import SmsParser
from .actions_list import ACTIONS_LIST
from faker import Faker


class SmsParserTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.phone = self.faker.phone_number()

    def test_parse_is_create_new_user_when_username_is_valid(self):
        # Arrange
        username = self.faker.first_name()
        message = 'I am ' + username
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_user'])
        self.assertEqual(result['payload']['username'], username)

    def test_parse_is_create_new_user_when_username_is_invalid(self):
        # Arrange
        username = self.faker.first_name() + ' ' + self.faker.last_name()
        message = 'I am ' + username
        session = {}

        # Assert
        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_recommendation_for_me_when_valid(self):
        # Arrange
        title = ''.join(self.faker.words(4))
        message = 'recommend ' + title + ' to me'
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_recommendation_for_me'])
        self.assertEqual(result['payload']['name'], title)

    def test_parse_is_rec_for_me_when_valid(self):
        # Arrange
        title = ''.join(self.faker.words(4))
        message = 'rec ' + title + ' to me'
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_recommendation_for_me'])
        self.assertEqual(result['payload']['name'], title)

    def test_parse_is_recommendation_for_me_when_no_movie_name(self):
        # Arrange
        title = ''
        message = 'recommend ' + title + ' to me'
        session = {}

        # Act
        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_recommendation_for_another_user_when_valid(self):
        # Arrange
        username = self.faker.first_name()
        title = ''.join(self.faker.words(4))
        message = 'recommend ' + title + ' to ' + username
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_recommendation_for_another_user'])
        self.assertEqual(result['payload']['name'], title)
        self.assertEqual(result['payload']['recommendee_username'], username)
        self.assertEqual(result['payload']['recommender_phone'], self.phone)

    def test_parse_is_rec_for_another_user_when_valid(self):
        # Arrange
        username = self.faker.first_name()
        title = ''.join(self.faker.words(4))
        message = 'rec ' + title + ' to ' + username
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['create_recommendation_for_another_user'])
        self.assertEqual(result['payload']['name'], title)
        self.assertEqual(result['payload']['recommendee_username'], username)
        self.assertEqual(result['payload']['recommender_phone'], self.phone)

    def test_parse_is_recommendation_for_another_user_when_no_movie_name(self):
        # Arrange
        username = self.faker.first_name()
        title = ''
        message = 'recommend ' + title + ' to ' + username
        session = {}

        # Act
        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_recommendation_acception_when_valid(self):
        # Arrange
        recommendation_id = str(self.faker.pyint())
        message = 'r' + recommendation_id
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['accept_recommendation_from_another_user'])
        self.assertEqual(result['payload']['recommendation_id'], recommendation_id)
        self.assertEqual(result['payload']['phone'], self.phone)

    def test_parse_is_recommendation_acception_when_no_recommendation_id(self):
        # Arrange
        message = 'r'
        session = {}

        # Assert
        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_view_list_when_valid(self):
        # Arrange
        message = 'list'
        session = {}

        # Act
        result = SmsParser.parse(message, self.phone, session)

        # Assert
        self.assertEqual(result['action'], ACTIONS_LIST['view_list'])
        self.assertEqual(result['payload']['phone'], self.phone)

    def test_parse_is_view_list_when_invalid(self):
        # Arrange
        message = 'lis t'
        session = {}

        # Assert
        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_invite(self):
        # Unfortunately, fakers phone numbers have extensions, which we don't support for now
        # invite_number = self.faker.phone_number()
        invite_number = '999-555-3322'
        message = f'invite {invite_number}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['invite'])
        self.assertEqual(result['payload']['invite_number'], invite_number)

    def test_parse_invite_when_invalid_invite_number(self):
        invite_number = '773 555 55'
        message = f'invite {invite_number}'
        session = {}

        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_add_context(self):
        message = ''.join(self.faker.words(5))
        session = {'latest_recommendation_id': self.faker.pyint()}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['add_context'])
        self.assertEqual(result['payload']['context'], message)
        self.assertEqual(result['payload']['session'], session)

    def test_parse_is_view_single_recommendation(self):
        position = str(self.faker.pyint())
        message = f'Show {position}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['view_single_recommendation'])
        self.assertEqual(result['payload']['position_in_list'], position)

    def test_parse_is_view_single_recommendation_when_no_list_position(self):
        message = f'Show '
        session = {}

        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

    def test_parse_is_delete(self):
        position = str(self.faker.pyint())
        message = f'Delete {position}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['delete'])
        self.assertEqual(result['payload']['position_in_list'], position)

    def test_parse_ask_from_another_user(self):
        askee_username = self.faker.first_name()
        message = f'ask {askee_username}'
        session = {}

        result = SmsParser.parse(message, self.phone, session)

        self.assertEqual(result['action'], ACTIONS_LIST['ask_from_another_user'])
        self.assertEqual(result['payload']['askee_username'], askee_username)

    def test_parse_ask_from_another_user_when_no_user_name(self):
        message = f'ask '
        session = {}

        self.assertRaises(ValueError, SmsParser.parse, message, self.phone, session)

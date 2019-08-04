from django.test import TestCase
from unittest import skip
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

    @skip("known bug #47")
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

    @skip("known bug #48")
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

    @skip("known bug #48")
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

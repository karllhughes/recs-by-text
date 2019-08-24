from django.test import TestCase
from faker import Faker
from unittest.mock import patch
from .delete_from_list import DeleteFromList


class DeleteFromListTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.phone = self.faker.phone_number()

    @patch('recommendations.models.User.objects')
    def test_execute_returns_message_when_deleted_successfully(self, mock_user):
        # Arrange
        name = ''.join(self.faker.words(4))
        mock_user.get().recommendations_recieved.filter().order_by().__getitem__().name = name
        payload = {
            'phone': self.phone,
            'position_in_list': str(self.faker.pyint()),
            'session': {}
        }

        # Act
        result = DeleteFromList.execute(payload)

        # Assert
        mock_user.get().recommendations_recieved.filter().order_by().__getitem__().delete.assert_called_once()
        self.assertIn("'" + name + "'", result['message'])

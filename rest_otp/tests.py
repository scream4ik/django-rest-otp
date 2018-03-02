from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from .helpers import tmp_user_id


class SetUpUserMixin:
    """
    Mixin class for user setup
    """

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(username='user')


class LoginOtpViewTest(SetUpUserMixin, APITestCase):
    """
    Tests for LoginOtpView
    """

    def test_post_success(self):
        """
        test for post request to login_otp
        :return: 200
        """
        tmp_data = tmp_user_id(self.user.id)

        data = {
            'tmp_user_id': tmp_data['tmp_user_id']['otp'],
            'otp_code': self.user.otp.get_otp_code()
        }
        response = self.client.post(
            reverse('login_otp'), data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_post_fail(self):
        """
        test for post request to login_otp
        :return: 200
        """
        tmp_data = tmp_user_id(self.user.id)

        data = {
            'tmp_user_id': tmp_data['tmp_user_id']['otp'],
            'otp_code': 'otp fail code'
        }
        response = self.client.post(reverse('login_otp'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginRecoveryCodeViewTest(SetUpUserMixin, APITestCase):
    """
    Tests for LoginRecoveryCodeView
    """

    def test_post_success(self):
        """
        test for post request to login_recovery_code
        :return: 200
        """
        tmp_data = tmp_user_id(self.user.id)

        data = {
            'tmp_user_id': tmp_data['tmp_user_id']['recovery'],
            'recovery_code': self.user.recovery_codes.first().code
        }
        response = self.client.post(reverse('login_recovery_code'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_post_fail(self):
        """
        test for post request to login_recovery_code
        :return: 200
        """
        tmp_data = tmp_user_id(self.user.id)

        data = {
            'tmp_user_id': tmp_data['tmp_user_id']['recovery'],
            'recovery_code': 'recovery code'
        }
        response = self.client.post(reverse('login_recovery_code'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

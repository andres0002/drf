# py
# django
# drf
from rest_framework import status
from rest_framework.test import APITestCase
# third
# own

class TestSetUp(APITestCase):
    def setUp(self):
        from apps.features.user.models import Users
        self.login_url = '/auth/login/'
        self.user = Users.objects.create_superuser(
            username = 'test',
            email = 'test@yopmail.com',
            name = 'test',
            lastname = 'lastname',
            phone = '0123456789',
            password = '12345'
        )
        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': '12345'
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # para para el code en ese punto -> y se puede hacer el response.data.
        # import pdb; pdb.set_trace()
        self.token = response.data['token']
        # authtoken.
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # jwt.
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        return super().setUp()
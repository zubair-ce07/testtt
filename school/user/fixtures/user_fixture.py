from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from faker import Faker


class UserFixture():

    def get_user_data(self):
        
        fake = Faker()
        password = fake.password()
        return {
                'username': fake.first_name(),
                'password1': password,
                'password2': password
                }
    
    def create_user_token(self):
        
        user_data = self.get_user_data()
        
        client = APIClient()
        response = client.post(
            reverse('rest_register'),
            user_data,
            format="json")
        if (response.status_code == 201):
            return response.data['key']

        

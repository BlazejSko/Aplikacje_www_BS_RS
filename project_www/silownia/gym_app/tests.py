from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from . import views
from .models import Gym, Classrooms
from rest_framework import status
from django.utils.http import urlencode
from django import urls
from django.contrib.auth.models import User

# Create your tests here.


class GymTests(APITestCase):
    def post_gym(self, address, phone_number, email_address, client):
        url = reverse(views.GymList.name)
        data = {'address': address, 'phone_number': phone_number, 'email_address': email_address}
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_gym(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        response = self.post_gym(new_address, new_phone_number, new_email_address, client)
        assert response.status_code == status.HTTP_201_CREATED
        assert Gym.objects.count() == 1
        assert Gym.objects.get().address == new_address

    def test_post_existing_gym(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        response_one = self.post_gym(new_address, new_phone_number, new_email_address, client)
        assert response_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_gym(new_address, new_phone_number, new_email_address, client)
        assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_gyms_collection(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        self.post_gym(new_address, new_phone_number, new_email_address, client)
        url = reverse(views.GymList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['address'] == new_address

    def test_update_gym(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)

        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        response = self.post_gym(new_address, new_phone_number, new_email_address, client)

        url = urls.reverse(views.GymDetail.name, None, {response.data['id']})
        updated_gym_address = 'Mragowska 16'
        updated_phone_number = '123456733'
        updated_email_address = 'pakernia@kozak.com'
        data = {'address': updated_gym_address,
                'phone_number': updated_phone_number,
                'email_address': updated_email_address}
        patch_response = client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['address'] == updated_gym_address

    def test_get_gym(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)

        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        response = self.post_gym(new_address, new_phone_number, new_email_address, client)

        url = urls.reverse(views.GymDetail.name, None, {response.data['id']})
        get_response = client.patch(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['address'] == new_address


class ClassroomsTests(APITestCase):
    def create_gym(self, address, phone_number, email_address, client):
        url = reverse(views.GymList.name)
        data = {'address': address,
                'phone_number': phone_number,
                'email_address': email_address}
        client.post(url, data, format='json')

    def post_classroom(self, gym, name, client):
        url = reverse(views.ClassroomList.name)
        data = {'gym': gym, 'name': name}
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_classroom(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        self.create_gym(new_address, new_phone_number, new_email_address, client)
        new_classroom_name = 'classroom name'
        response = self.post_classroom(new_address, new_classroom_name, client)
        assert response.status_code == status.HTTP_201_CREATED
        assert Classrooms.objects.count() == 1
        assert Classrooms.objects.get().name == new_classroom_name

    def test_post_existing_classroom(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        self.create_gym(new_address, new_phone_number, new_email_address, client)
        new_classroom_name = 'classroom name'
        response_one = self.post_classroom(new_address, new_classroom_name, client)
        assert response_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_classroom(new_address, new_classroom_name, client)
        assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_classrooms_collection(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        self.create_gym(new_address, new_phone_number, new_email_address, client)
        new_classroom_name = 'classroom name'
        self.post_classroom(new_address, new_classroom_name, client)
        url = reverse(views.ClassroomList.name)
        response = client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_classroom_name

    def test_update_classroom(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        self.create_gym(new_address, new_phone_number, new_email_address, client)
        new_classroom_name = 'classroom name'
        response = self.post_classroom(new_address, new_classroom_name, client)

        url = urls.reverse(views.ClassroomDetail.name, None, {response.data['id']})
        updated_classroom_name = 'Nowa nazewka'
        data = {'name': updated_classroom_name,
                'gym': new_address
                }
        patch_response = client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == updated_classroom_name

    def test_get_gym(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.force_authenticate(user=user)
        new_address = 'Polna 23'
        new_phone_number = '123456789'
        new_email_address = 'pakernia@koksu.com'
        self.create_gym(new_address, new_phone_number, new_email_address, client)
        new_classroom_name = 'classroom name'
        response = self.post_classroom(new_address, new_classroom_name, client)

        url = urls.reverse(views.ClassroomDetail.name, None, {response.data['id']})
        get_response = client.patch(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == new_classroom_name

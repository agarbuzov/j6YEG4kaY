from django.test import TestCase, Client
from django.urls import reverse
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.read_url = reverse('read')
        self.delete_url = reverse('delete')
        self.create_url = reverse('create')

    def test_delete_view(self):
        response = self.client.post(self.delete_url, data={"keys": ["key2"]})
        self.assertEqual(response.status_code, 200)

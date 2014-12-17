"""
Tests for groups
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory


class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/groups/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_get_app_groups(self):
        url = reverse('get-app-groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('groups' in response.data)  # pylint: disable=E1103

    def test_create_new_group(self):
        url = reverse('create-new-group') 
        response = self.client.post(url, {  'name' : 'TheBestGroup', 
                                            'description' : 'The group for the best people',
                                            'privacy' : 'true',
                                            'admin-id' : '12345',
                                            'oauth-token' : 'abcd1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('TheBestGroup' in response.data['name'])  # pylint: disable=E1103

    def test_invite_one_member(self):
        url = reverse('invite-to-group', kwargs={'group_id':'123456789'}) 
        response = self.client.post(url, {'member': '121212'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('true' in response.data['success'])  # pylint: disable=E1103

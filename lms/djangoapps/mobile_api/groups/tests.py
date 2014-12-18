"""
Tests for groups
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory

from nose.tools import set_trace

from nose.tools import set_trace

class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/groups/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_get_app_groups(self):
        # set_trace()
        url = reverse('get-app-groups')
        response = self.client.get(url, {'oauth-token' : 'abcd1234'})
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
        self.assertTrue('12345' in response.data['group-id'])  # pylint: disable=E1103

    def test_invite_members(self):
        url = reverse('invite-to-group', kwargs={'group_id':'123456789'}) 
        response = self.client.post(url, {  'member-ids': '1,2,3,4,5,6',
                                            'oauth-token' : 'abcd1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('true' in response.data['success'])  # pylint: disable=E1103

    def test_get_all_group_members(self):
        # set_trace() 
        url = reverse('members-in-group', kwargs={'group_id':'123456789'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('members' in response.data)  # pylint: disable=E1103

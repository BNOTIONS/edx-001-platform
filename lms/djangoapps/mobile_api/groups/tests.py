"""
Tests for groups
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory

from nose.tools import set_trace


class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/groups/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_create_new_group(self):
        url = reverse('create-new-group')
        response = self.client.post(url, {  'name' : 'TheBestGroup',
                                            'description' : 'The group for the best people',
                                            'privacy' : 'open'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in response.data)  # pylint: disable=E1103

    def test_create_new_group_invalid_params(self):
        url = reverse('create-new-group')
        response = self.client.post(url, {  'invalid_param' : 'TheBestGroup'})
        self.assertEqual(response.status_code, 400)

    def test_create_new_group_no_params(self):
        url = reverse('create-new-group')
        set_trace()
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)
        # self.assertTrue('id' in response.data)  # pylint: disable=E1103

    def test_invite_members(self):
        url = reverse('invite-to-group', kwargs={'group_id':'123456789'}) 
        response = self.client.post(url, {  'member-ids': '1,2,3,4,5,6',
                                            'oauth-token' : 'abcd1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('true' in response.data['success'])  # pylint: disable=E1103

"""
Tests for groups
"""
# TODO: clean up imports
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory
from courseware.tests.tests import TEST_DATA_MONGO_MODULESTORE

from nose.tools import set_trace


class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/groups/...
    """
    def setUp(self):
        # super(TestVideoOutline, self).setUp()
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_get_app_groups(self):
        url = reverse('get-app-groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('groups' in response.data)  # pylint: disable=E1103

    def test_create_new_group(self):
        url = reverse('create-new-group') 
        response = self.client.post(url, {'group-id': '123456789'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('123456789' in response.data['group-id'])  # pylint: disable=E1103

    def test_invite_one_member(self):
        url = reverse('invite-to-group', kwargs={'group_id':'123456789'}) 
        # set_trace()
        response = self.client.post(url, {'member': '121212'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('121212' in response.data['member'])  # pylint: disable=E1103

"""
Tests for course_info
"""
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory

from nose.tools import set_trace
class TestFriends(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/friends/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_friends(self):
        url = reverse('courses-with-friends')
        response = self.client.get(url)
        # set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('courses' in response.data)  # pylint: disable=E1103
        self.assertTrue('course' in response.data['courses'][0])  # pylint: disable=E1103

    def test_friends_in_course(self):
        url = reverse('friends-in-course', kwargs={"course_id": "12345"})
        response = self.client.get(url)
        # set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data)
        self.assertTrue('id' in response.data['friends'][0])

    def test_friends_in_group(self):
        url = reverse('friends-in-group', kwargs={"group_id": "12345"})
        response = self.client.get(url)
        # set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data)
        self.assertTrue('id' in response.data['friends'][0])

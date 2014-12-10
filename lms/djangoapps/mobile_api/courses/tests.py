"""
Tests for Courses
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory


class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/courses/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_share_courses_set_to_true(self):
        url = reverse('share_settings')
        response = self.client.post(url, {'share_courses' : 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('true' in response.data['share_courses'])  # pylint: disable=E1103

    def test_share_courses_set_to_false(self):
        url = reverse('share_settings')
        response = self.client.post(url, {'share_courses' : 'false'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('false' in response.data['share_courses'])  # pylint: disable=E1103

    def test_friends(self):
        url = reverse('courses-with-friends')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('courses' in response.data)  # pylint: disable=E1103
        self.assertTrue('course' in response.data['courses'][0])  # pylint: disable=E1103
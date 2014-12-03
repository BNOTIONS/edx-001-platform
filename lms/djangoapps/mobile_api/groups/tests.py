"""
Tests for groups
"""
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory
from courseware.tests.tests import TEST_DATA_MONGO_MODULESTORE


@override_settings(MODULESTORE=TEST_DATA_MONGO_MODULESTORE)
class TestVideoOutline(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/groups/...
    """
    def setUp(self):
        super(TestVideoOutline, self).setUp()
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_get_app_groups(self):
        url = reverse('get-app-groups')
        response = self.client.get(url)
        # self.assertTrue(False)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('groups' in response.data)  # pylint: disable=E1103

    # def test_create_new_group(self):
    #     url = reverse('create-new-group', kwargs={'group_name': "The Best Group Name"}) 
    #     response = self.client.get(url)
    #     self.assertTrue(False)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('groups' in response.data)  # pylint: disable=E1103
"""
Tests for users sharing preferences
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

from user_api.api import account as account_api
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase


class StudentProfileViewTest(ModuleStoreTestCase, TestCase):
    """ Tests for the student profile views. """

    USERNAME = u'bnotions'
    PASSWORD = u'horse'
    EMAIL = u'horse@bnotions.com'
    FULL_NAME = u'bnotions horse'


    def setUp(self):
        super(StudentProfileViewTest, self).setUp()

        # Create/activate a new account
        activation_key = account_api.create_account(self.USERNAME, self.PASSWORD, self.EMAIL)
        account_api.activate_account(activation_key)

        # Login
        result = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(result)

    def test_set_preferences_to_true(self):
        url = reverse('share_pref')
        response = self.client.post(url, {'share_pref' : 'True'})
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('True' in response.data['share_pref'])

    def test_set_preferences_to_false(self):
        url = reverse('share_pref')
        response = self.client.post(url, {'share_pref' : 'False'})
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('False' in response.data['share_pref'])
    
    def test_set_preferences_no_parameters(self):
        # Note that if no value is given it will default to True
        url = reverse('share_pref')
        response = self.client.post(url, { })
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('True' in response.data['share_pref'])

    def test_set_preferences_invalid_parameters(self):
        # Note that if no value is given it will default to True 
        # also in the case of invalid parameters 
        # TODO: check this! 
        url = reverse('share_pref')
        response = self.client.post(url, {'bad_param' : 'False'})
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('True' in response.data['share_pref'])

    def test_get_preferences(self):
        # Note that if no value is given it will default to True
        url = reverse('share_pref')
        response = self.client.post(url, { })
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('True' in response.data['share_pref'])


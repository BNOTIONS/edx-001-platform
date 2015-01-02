"""
Tests for users sharing preferences
"""

from urllib import urlencode
import json

from mock import patch
import ddt
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from util.testing import UrlResetMixin
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from user_api.api import account as account_api
from user_api.api import profile as profile_api
from lang_pref import LANGUAGE_KEY, api as language_api


from nose.tools import set_trace

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
        url = reverse('user_sharing')
        response = self.client.post(url, {'share_pref' : 'true'})
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('true' in response.data['share_pref'])

    def test_set_preferences_to_false(self): 
        url = reverse('user_sharing')
        response = self.client.post(url, {'share_pref' : 'false'})
        self.assertTrue('share_pref' in response.data)
        self.assertTrue('false' in response.data['share_pref'])


    # def _change_preferences(self, **preferences):
    #     """Request a change to the user's preferences.

    #     Returns:
    #         HttpResponse

    #     """
    #     data = {}
    #     for key, value in preferences.iteritems():
    #         if value is not None:
    #             data[key] = value

    #     return self.client.put(
    #         path=reverse('preference_handler'),
    #         data=urlencode(data),
    #         content_type='application/x-www-form-urlencoded'
    #     )

"""
Tests for friends
"""
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory
from xmodule.modulestore.tests.factories import CourseFactory
from rest_framework import status
from django.test.client import Client
import json
from student.models import CourseEnrollment
from social.apps.django_app.default.models import UserSocialAuth
from nose.tools import set_trace
from student.views import login_oauth_token

import httpretty


class TestFriends(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/friends/...
    """
    USERNAME_1 = "Daniel Eidan"
    EMAIL_1 = "daniel@ebnotions.com"
    PASSWORD_1 = "edx"
    FB_ID_1 = "10155110991745300"

    USERNAME_2 = "Marc Ashman"
    EMAIL_2 = "marc@ebnotions.com"
    PASSWORD_2 = "edx"
    FB_ID_2 = "10154833899435243"

    USERNAME_3 = "Peter Organa"
    EMAIL_3 = "peter@ebnotions.com"
    PASSWORD_3 = "edx"
    FB_ID_3 = "10154805420820176"

    BACKEND = "facebook"
    USER_URL = "https://graph.facebook.com/me"
    UID_FIELD = "id"

    _FB_USER_ACCESS_TOKEN = 'CAAKbz9eIdVsBABmFt9kSO34MkLI0AwuLemGbwXLgxoYbmTXuh1sKIuGoZAjeK1XdIHMBoURsll0iq1OG7Jpz0B1iHuk4OYvhSgJdFihaNqOkHM8HHlNXjTUODjUn3ol5s4lYDP5NpDR1wUHCocZCBUWuZABBW3BNR5oDwypTVjAU7OjXnTZCBagsGuv1CEKPTIE5EcvUanQmuJEE02Ta'


    def setUp(self):
        super(TestFriends, self).setUp()
        self.course = CourseFactory.create()

    @httpretty.activate
    def test_no_friends_in_course_because_no_friends_enrolled(self):
        # User 1 set up
        self.user_create_and_signin(1)
        # Link user_1's edX account to FB
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        # Set the interceptor 
        self.set_facebook_interceptor({'data': [{   
                                            'name': self.USERNAME_1,
                                            'id':   self.FB_ID_1}, 
                                        {   'name': self.USERNAME_2,
                                            'id':   self.FB_ID_2}, 
                                        {   'name': self.USERNAME_3, 
                                            'id': self.FB_ID_3}
                                            ]})
        course_id = self.format_course_id()
        url = reverse('friends-in-course', kwargs={"course_id": course_id})
        response = self.client.get(url, {   'format' : 'json', 
                                            'oauth-token' : self._FB_USER_ACCESS_TOKEN})
        
        # Assert that no friends are returned
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data and len(response.data['friends']) == 0)

    @httpretty.activate
    def test_no_friends_in_course_because_no_friends_on_facebook(self):
        # User 1 set up
        self.user_create_and_signin(1)
        # Enroll user_1 in the course
        self.enroll_in_course(self.user_1, self.course)
        # Link user_1's edX account to FB
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        # Set the interceptor 
        self.set_facebook_interceptor({'data': []})
        course_id = self.format_course_id()
        url = reverse('friends-in-course', kwargs={"course_id": course_id})
        response = self.client.get(url, {   'format' : 'json', 
                                            'oauth-token' : self._FB_USER_ACCESS_TOKEN})
        
        # Assert that no friends are returned
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data and len(response.data['friends']) == 0)


    def test_no_friends_in_course_because_no_friends_on_facebook_linked_to_edX(self):
        # User 1 set up
        self.user_create_and_signin(1)
        # Enroll user_1 in the course
        self.enroll_in_course(self.user_1, self.course)
        # User 2 set up
        self.user_create_and_signin(2)
        # Enroll user_2 in the course
        self.enroll_in_course(self.user_2, self.course)
        # User 3 set up
        self.user_create_and_signin(3)
        # Enroll user_3 in the course
        self.enroll_in_course(self.user_3, self.course)

        # Set the interceptor 
        self.set_facebook_interceptor({'data': [{   
                                            'name': self.USERNAME_1,
                                            'id':   self.FB_ID_1}, 
                                        {   'name': self.USERNAME_2,
                                            'id':   self.FB_ID_2}, 
                                        {   'name': self.USERNAME_3, 
                                            'id': self.FB_ID_3}
                                            ]})
        
        course_id = self.format_course_id()
        url = reverse('friends-in-course', kwargs={"course_id": course_id})
        response = self.client.get(url, {   'format' : 'json', 
                                            'oauth-token' : self._FB_USER_ACCESS_TOKEN})
        
        # Assert that no friends are returned
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data and len(response.data['friends']) == 0)

    @httpretty.activate
    def test_one_friend_in_course(self):
        # set_trace()
        # User 1 set up
        self.user_create_and_signin(1)
        # Enroll user_1 in the course
        self.enroll_in_course(self.user_1, self.course)
        # link user_1's edX account to FB
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        
        # Set the interceptor 
        self.set_facebook_interceptor({'data': [{   'name': self.USERNAME_1,
                                        'id':   self.FB_ID_1}, 
                                    {   'name': self.USERNAME_2,
                                        'id':   self.FB_ID_2}, 
                                    {   'name': self.USERNAME_3, 
                                        'id': self.FB_ID_3}
                                    ]})

        course_id = self.format_course_id()
        url = reverse('friends-in-course', kwargs={"course_id": course_id})
        response = self.client.get(url, {   'format' : 'json', 
                                            'oauth-token' : self._FB_USER_ACCESS_TOKEN})
        
        # Assert that USERNAME_1 is returned
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data)
        self.assertTrue('id' in response.data['friends'][0] and response.data['friends'][0]['id'] == self.FB_ID_1)
        self.assertTrue('name' in response.data['friends'][0] and response.data['friends'][0]['name'] == self.USERNAME_1)

    @httpretty.activate
    def test_three_friends_in_course(self):
        # User 1 set up
        self.user_create_and_signin(1)
        # Enroll user_1 in the course
        self.enroll_in_course(self.user_1, self.course)
        # link user_1's edX account to FB
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        
        # User 2 set up
        self.user_create_and_signin(2)
        # Enroll user_1 in the course
        self.enroll_in_course(self.user_2, self.course)
        # link user_1's edX account to FB
        self.link_edX_account_to_social_backend(self.user_2, self.BACKEND, self.FB_ID_2)

        # User 3 set up
        self.user_create_and_signin(3)
        # Enroll user_1 in the course
        self.enroll_in_course(self.user_3, self.course)
        # link user_1's edX account to FB
        self.link_edX_account_to_social_backend(self.user_3, self.BACKEND, self.FB_ID_3)

        # Set the interceptor 
        self.set_facebook_interceptor({'data': [{   'name': self.USERNAME_1,
                                        'id':   self.FB_ID_1}, 
                                    {   'name': self.USERNAME_2,
                                        'id':   self.FB_ID_2}, 
                                    {   'name': self.USERNAME_3, 
                                        'id': self.FB_ID_3}
                                    ]})

        course_id = self.format_course_id()
        url = reverse('friends-in-course', kwargs={"course_id": course_id})
        response = self.client.get(url, {   'format' : 'json', 
                                            'oauth-token' : self._FB_USER_ACCESS_TOKEN})
        
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('friends' in response.data)
        # Assert that USERNAME_1 is returned
        self.assertTrue('id' in response.data['friends'][0] and response.data['friends'][0]['id'] == self.FB_ID_1)
        self.assertTrue('name' in response.data['friends'][0] and response.data['friends'][0]['name'] == self.USERNAME_1)
        # Assert that USERNAME_2 is returned
        self.assertTrue('id' in response.data['friends'][1] and response.data['friends'][1]['id'] == self.FB_ID_2)
        self.assertTrue('name' in response.data['friends'][1] and response.data['friends'][1]['name'] == self.USERNAME_2)
        # Assert that USERNAME_3 is returned
        self.assertTrue('id' in response.data['friends'][2] and response.data['friends'][2]['id'] == self.FB_ID_3)
        self.assertTrue('name' in response.data['friends'][2] and response.data['friends'][2]['name'] == self.USERNAME_3)


    def set_facebook_interceptor(self, data): 
        httpretty.register_uri(httpretty.GET, 
                        "https://graph.facebook.com/v2.2/me/friends",
                        body=json.dumps(data),
                        status=201)

    def user_create_and_signin(self, user_number): 
        if user_number == 1:
            self.user_1 = UserFactory.create(   username=self.USERNAME_1, 
                                                email=self.EMAIL_1, 
                                                password=self.PASSWORD_1)
            self.client.login(username=self.USERNAME_1, password=self.PASSWORD_1)
        elif user_number == 2:
            self.user_2 = UserFactory.create(   username=self.USERNAME_2, 
                                                email=self.EMAIL_2, 
                                                password=self.PASSWORD_2)
            self.client.login(username=self.USERNAME_2, password=self.PASSWORD_2)
        elif user_number == 3:
            self.user_3 = UserFactory.create(   username=self.USERNAME_3, 
                                                email=self.EMAIL_3, 
                                                password=self.PASSWORD_3)
            self.client.login(username=self.USERNAME_3, password=self.PASSWORD_3)

    def enroll_in_course(self, user, course): 
        resp = self._change_enrollment('enroll')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(CourseEnrollment.is_enrolled(user, course.id))
        course_mode, is_active = CourseEnrollment.enrollment_mode_for_user(user, course.id)
        self.assertTrue(is_active)
        self.assertEqual(course_mode, 'honor')

    def link_edX_account_to_social_backend(self, user, backend, social_uid):
        self.url = reverse(login_oauth_token, kwargs={"backend": backend})
        # self.social_uid = "10155110991745300"
        UserSocialAuth.objects.create(user=user, provider=backend, uid=social_uid)

    def format_course_id(self): 
        return self.course.scope_ids.usage_id.course_key._to_string().replace('+', '/')

    def _change_enrollment(self, action, course_id=None, email_opt_in=None):
        """Change the student's enrollment status in a course.

        Args:
            action (string): The action to perform (either "enroll" or "unenroll")

        Keyword Args:
            course_id (unicode): If provided, use this course ID.  Otherwise, use the
                course ID created in the setup for this test.
            email_opt_in (unicode): If provided, pass this value along as
                an additional GET parameter.

        Returns:
            Response

        """
        if course_id is None:
            course_id = unicode(self.course.id)

        params = {
            'enrollment_action': action,
            'course_id': course_id
        }

        if email_opt_in:
            params['email_opt_in'] = email_opt_in

        return self.client.post(reverse('change_enrollment'), params)

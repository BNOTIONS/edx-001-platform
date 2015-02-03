"""
Tests for Courses
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory
from xmodule.modulestore.tests.factories import CourseFactory
from student.models import CourseEnrollment
from student.views import login_oauth_token
from social.apps.django_app.default.models import UserSocialAuth
import httpretty
import json
from openedx.core.djangoapps.user_api.api.profile import preference_info, update_preferences


class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/courses/...
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

    # TODO: Needs to be a valid access token
    _FB_USER_ACCESS_TOKEN = 'CAAKbz9eIdVsBABmFt9kSO34MkLI0AwuLemGbwXLgxoYbmTXuh1sKIuGoZAjeK1XdIHMBoURsll0iq1OG7Jpz0B1iHuk4OYvhSgJdFihaNqOkHM8HHlNXjTUODjUn3ol5s4lYDP5NpDR1wUHCocZCBUWuZABBW3BNR5oDwypTVjAU7OjXnTZCBagsGuv1CEKPTIE5EcvUanQmuJEE02Ta'

    def setUp(self):
        super(TestGroups, self).setUp()
        self.course = CourseFactory.create(mobile_available=True)

    @httpretty.activate
    def test_one_courses_with_friends(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, True)
        self.set_facebook_interceptor({'data':
                                        [{'name': self.USERNAME_1,
                                            'id': self.FB_ID_1}
                                        ]})
        self.enroll_in_course(self.user_1, self.course)
        url = reverse('courses-with-friends')
        response = self.client.get(url, {'oauth_token': self._FB_USER_ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.id._to_string().replace('+', '/'),
                         response.data[0]['course']['id'])

    @httpretty.activate
    def test_two_courses_with_friends(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, True)
        self.enroll_in_course(self.user_1, self.course)
        self.course_2 = CourseFactory.create(mobile_available=True)
        self.enroll_in_course(self.user_1, self.course_2)
        self.set_facebook_interceptor({'data':
                                        [{'name': self.USERNAME_1,
                                            'id': self.FB_ID_1}
                                        ]})
        url = reverse('courses-with-friends')
        response = self.client.get(url, {'oauth_token': self._FB_USER_ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.id._to_string().replace('+', '/'),
                         response.data[0]['course']['id'])
        self.assertEqual(self.course_2.id._to_string().replace('+', '/'),
                         response.data[1]['course']['id'])

    @httpretty.activate
    def test__three_courses_but_only_two_unique(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, True)
        self.course_2 = CourseFactory.create(mobile_available=True)
        self.enroll_in_course(self.user_1, self.course_2)
        self.enroll_in_course(self.user_1, self.course)
        self.user_create_and_signin(2)
        self.link_edX_account_to_social_backend(self.user_2, self.BACKEND, self.FB_ID_2)
        self.set_sharing_preferences(self.user_2, True)
        # Enroll another user in course_2
        self.enroll_in_course(self.user_2, self.course_2)
        self.set_facebook_interceptor({'data':
                                        [{'name': self.USERNAME_1,
                                            'id': self.FB_ID_1},
                                        {'name': self.USERNAME_2,
                                            'id': self.FB_ID_2}
                                        ]})
        url = reverse('courses-with-friends')
        response = self.client.get(url, {'oauth_token': self._FB_USER_ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.id._to_string().replace('+', '/'),
                         response.data[0]['course']['id'])
        self.assertEqual(self.course_2.id._to_string().replace('+', '/'),
                         response.data[1]['course']['id'])
        # Assert that only two courses are returned
        self.assertEqual(len(response.data), 2)

    @httpretty.activate
    def test_two_courses_with_two_friends_on_different_paged_results(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, True)
        self.enroll_in_course(self.user_1, self.course)

        self.user_create_and_signin(2)
        self.link_edX_account_to_social_backend(self.user_2, self.BACKEND, self.FB_ID_2)
        self.set_sharing_preferences(self.user_2, True)
        self.course_2 = CourseFactory.create(mobile_available=True)
        self.enroll_in_course(self.user_2, self.course_2)

        self.set_facebook_interceptor({'data':
                                        [{'name': self.USERNAME_1,
                                            'id': self.FB_ID_1}],
                                        "paging": {
                                             "next": "https://graph.facebook.com/v2.2/me/friends/next"
                                        },
                                        "summary": {
                                                "total_count": 652
                                          }
                                    })
        # Set the interceptor for the paged 
        httpretty.register_uri( httpretty.GET,
                                "https://graph.facebook.com/v2.2/me/friends/next",
                                body=json.dumps({"data": [ {'name': self.USERNAME_2,
                                                            'id': self.FB_ID_2}],
                                                "paging": {"previous": "https://graph.facebook.com/v2.2/10154805434030300/friends?limit=25&offset=25"},
                                                "summary": {"total_count": 652}
                                                }),
                                status=201)

        url = reverse('courses-with-friends')
        response = self.client.get(url, {'oauth_token': self._FB_USER_ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.id._to_string().replace('+', '/'),
                         response.data[0]['course']['id'])
        self.assertEqual(self.course_2.id._to_string().replace('+', '/'),
                         response.data[1]['course']['id'])

    @httpretty.activate
    def test_no_courses_with_friends_beacause_sharring_pref_off(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, False)
        self.set_facebook_interceptor({'data':
                                        [{'name': self.USERNAME_1,
                                            'id': self.FB_ID_1}
                                        ]})
        self.enroll_in_course(self.user_1, self.course)
        url = reverse('courses-with-friends')
        response = self.client.get(url, {'oauth_token': self._FB_USER_ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    @httpretty.activate
    def test_no_courses_with_friends_beacause_no_auth_token(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, False)
        self.set_facebook_interceptor({'data':
                                        [{'name': self.USERNAME_1,
                                            'id': self.FB_ID_1}
                                        ]})
        self.enroll_in_course(self.user_1, self.course)
        url = reverse('courses-with-friends')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_no_courses_with_friends_beacause_bad_auth_token(self):
        self.user_create_and_signin(1)
        self.link_edX_account_to_social_backend(self.user_1, self.BACKEND, self.FB_ID_1)
        self.set_sharing_preferences(self.user_1, False)
        self.enroll_in_course(self.user_1, self.course)
        url = reverse('courses-with-friends')
        response = self.client.get(url, {'oauth_token': self._FB_USER_ACCESS_TOKEN + "this_is_a_bad_token"})
        self.assertEqual(response.status_code, 400)


    '''
        Helper Functions 
    '''

    def set_sharing_preferences(self, user, boolean_value):
        ''' Sets self.user's share settings to True
        '''
        update_preferences(user.username, share_pref=boolean_value)
        self.assertEqual(preference_info(user.username)['share_pref'], unicode(boolean_value))


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
        resp = self._change_enrollment('enroll', course_id=course.id)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(CourseEnrollment.is_enrolled(user, course.id))
        course_mode, is_active = CourseEnrollment.enrollment_mode_for_user(user, course.id)
        self.assertTrue(is_active)
        self.assertEqual(course_mode, 'honor')

    def link_edX_account_to_social_backend(self, user, backend, social_uid):
        self.url = reverse(login_oauth_token, kwargs={"backend": backend})
        UserSocialAuth.objects.create(user=user, provider=backend, uid=social_uid)

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

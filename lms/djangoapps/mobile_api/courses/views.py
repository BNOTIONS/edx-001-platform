"""
Views for courses info API
"""


from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
from student.models import CourseEnrollment
from courseware import models
from enrollment import api
from third_party_auth import pipeline, provider
from nose.tools import set_trace
from openedx.core.djangoapps.user_api.models import User, UserProfile, UserPreference, UserOrgTag
from opaque_keys.edx.locator import CourseLocator
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from social.apps.django_app.default.models import UserSocialAuth
from courseware.access import is_mobile_available_for_user
from mobile_api.users.serializers import CourseEnrollmentSerializer
from sets import Set

# TODO: dependencies to be added to the vagrant 
import facebook

# TODO: This should not be in the final commit
_APP_SECRET = "6c26348ef355f53a531890e980ddc731"
_APP_ID = "735343629893573"

_FACEBOOK_API_VERSION = "v2.2/"


class CoursesWithFriends(generics.ListAPIView):
    """
    **Use Case**

        API endpoint for retriving all the courses that a users friends are in. 
        Note that only friends that allow their courses to be shared will be included.

    **Example request**

        GET /api/mobile/v0.5/courses/friends

    **Response Values**

        [
            {   "created": "2014-12-09 16:58:31.926438",
            "mode": "honor",
            "is_active": "True",
            "course": {
                "course_about": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/about",
                "course_updates": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/updates",
                "number": "course_4",
                "org": "org.4",
                "video_outline": "http://testserver/api/mobile/v0.5/video_outlines/courses/org.4/course_4/Run_4",
                "id": "org.4/course_4/Run_4",
                "latest_updates": {
                    "video": "None"
                },
                "end": "None",
                "name": "Run 4",
                "course_handouts": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/handouts",
                "start": "2030-01-01 00:00:00",
                "course_image": "/c4x/org.4/course_4/asset/images_course_image.jpg"
                }
            },
            ...
        ]
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = CourseEnrollmentSerializer


    def list(self, request, *args, **kwargs):
        # set_trace()
        # get all the users FB friends
        oauth_token = self.get_token(request)
        if oauth_token:
            graph = facebook.GraphAPI(oauth_token)
            url = _FACEBOOK_API_VERSION + "me/friends"
            friends = graph.request(url)
            # TODO: deal with pagination
                    
            # For each friend check if they are a linked edX user
            friends_that_are_edX_users = []
            for friend in friends['data']:
                name = friend['name']
                fb_id = friend['id']
                query_set = UserSocialAuth.objects.filter(uid=unicode(fb_id))
                if query_set.count() == 1: 
                    friend['edX_id'] = query_set[0].user_id
                    friends_that_are_edX_users.append(friend)
            
            # For each edX friend check if they are a member of that course 
            # and if so add them to the result set
            enrollments = []
            for friend in friends_that_are_edX_users:
                query_set = CourseEnrollment.objects.filter(user_id = friend['edX_id'], 
                                                            is_active = True)
                if query_set.count() > 0:
                    for i in range(len(query_set)):
                        if not self.is_member(enrollments, query_set[i]):
                            enrollments.append(query_set[i])

            courses = [enrollment for enrollment in enrollments if enrollment.course and is_mobile_available_for_user(self.request.user, enrollment.course)]
            
            # TODO: filter based on TOC after merging with TOC branch

            # set_trace()
            serialized_courses = CourseEnrollmentSerializer(courses)
            return Response(serialized_courses.data)
        return Response({})

    def get_token(self, request): 
        if 'oauth-token' in request.GET:
            return request.GET['oauth-token']

    def is_member(self, enrollments, query_set_item):
        ''' Return true if the query_set_item is in enrollments
        '''
        for enrollment in enrollments:
            if query_set_item.course_id == enrollment.course_id:
                return True
        return False

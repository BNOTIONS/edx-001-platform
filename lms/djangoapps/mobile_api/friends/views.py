"""
Views for friends info API
"""

from rest_framework import generics, permissions, status
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
from openedx.core.djangoapps.user_api.models import User, UserProfile, UserPreference, UserOrgTag
from openedx.core.djangoapps.user_api.api.profile import preference_info
from opaque_keys.edx.locator import CourseLocator
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from social.apps.django_app.default.models import UserSocialAuth
from third_party_auth import pipeline, provider
from student.models import CourseEnrollment
from courseware import models
from enrollment import api
import serializers
import urllib2
import json
import facebook

# TODO: This should not be in the final commit
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"

_FACEBOOK_API_VERSION = "v2.2/"


class FriendsInCourse(generics.ListAPIView):
    """
    **Use Case**

        API endpoint that returns all the users friends that are in the course specified.
        Note that only friends that allow their courses to be shared will be included.

    **Example request**:

        GET /api/mobile/v0.5/friends/course/<course_id>

        where course_id is in the form of /edX/DemoX/Demo_Course

    **Response Values**

        {   "friends":
                [{
                    "name": "test",
                    "id": "12345",
                    "edX_id": "678910"
                },
                ...
                ]
            }
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FriendsInCourseSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET, files=request.FILES)
        if serializer.is_valid():
            # Get all the users FB friends
            graph = facebook.GraphAPI(serializer.object['oauth_token'])
            url = _FACEBOOK_API_VERSION + "me/friends"
            friends = graph.request(url)
            data = self.get_pagination(friends)
            # For each friend check if they are a linked edX user
            friends_that_are_edX_users = []
            for friend in data:
                query_set = UserSocialAuth.objects.filter(uid=unicode(friend['id']))
                if query_set.count() == 1: 
                    friend['edX_id'] = query_set[0].user_id
                    friend['edX_username'] = query_set[0].user.username
                    friends_that_are_edX_users.append(friend)
            # Filter by sharing preferences
            friends_that_are_edX_users_with_sharing = [friend for friend in friends_that_are_edX_users if self.sharing_pref_true(friend)]
            if ('course_id' in kwargs) and len(kwargs['course_id'].split('/')) == 3:
                course_path = kwargs['course_id'].split('/')
                course_key = SlashSeparatedCourseKey(course_path[0], course_path[1], course_path[2])
            fb_friends_in_course = [friend for friend in  friends_that_are_edX_users_with_sharing if self.is_member(course_key, friend)]
            return Response({'friends' : fb_friends_in_course})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def is_member(self, course_key, friend):
            return CourseEnrollment.objects.filter(course_id = course_key, 
                                                        user_id =  friend['edX_id'], 
                                                        is_active = True ).count() == 1

    def get_pagination(self, friends): 
        '''
            Get paginated data from response
        '''
        data = friends['data']
        while 'paging' in friends and 'next' in friends['paging']: 
            response = urllib2.urlopen(friends['paging']['next'])
            friends = json.loads(response.read())
            data = data + friends['data']
        return data

    def sharing_pref_true(self, friend):
        share_pref_setting = preference_info(friend['edX_username'])
        return ('share_pref' in share_pref_setting) and (share_pref_setting['share_pref'] == 'True')


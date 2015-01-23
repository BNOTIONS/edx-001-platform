"""
Views for friends info API
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
from openedx.core.djangoapps.user_api.api.profile import preference_info
import urllib2
import json


# TODO: dependencies to be added to the vagrant 
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

    def list(self, request, *args, **kwargs):
        # get all the users FB friends
        oauth_token = self.get_token(request)
        if oauth_token:
            graph = facebook.GraphAPI(oauth_token)
            url = _FACEBOOK_API_VERSION + "me/friends"
            friends = graph.request(url)
        
            # Pagination
            data = friends['data']
            while 'paging' in friends and 'next' in friends['paging']: 
                response = urllib2.urlopen(friends['paging']['next'])
                friends = json.loads(response.read())
                data = data + friends['data']
                    
            # For each friend check if they are a linked edX user
            friends_that_are_edX_users = []
            for friend in data:
                name = friend['name']
                fb_id = friend['id']
                query_set = UserSocialAuth.objects.filter(uid=unicode(fb_id))
                if query_set.count() == 1: 
                    friend['edX_id'] = query_set[0].user_id
                    friends_that_are_edX_users.append(friend)

            # Filter based on the users share preferences
            friends_that_are_edX_users_with_sharing = []
            for friend in friends_that_are_edX_users:
                share_pref_setting = preference_info(friend['name'])
                if 'share_pref' in share_pref_setting and share_pref_setting['share_pref'] == 'True':
                    friends_that_are_edX_users_with_sharing.append(friend)


            if 'course_id' in kwargs:
                course_path = kwargs['course_id'].split('/') 
                if len(course_path) == 3: 
                    ss_course_key = SlashSeparatedCourseKey(course_path[0], course_path[1], course_path[2])
                else:
                    #TODO: assert that this never happens   
                    pass
            else: 
                #TODO: assert that this never happens 
                pass
            
            # For each edX friend check if they are a member of that course 
            # and if so add them to the result set
            fb_friends_in_course = []
            for friend in friends_that_are_edX_users_with_sharing:
                query_set = CourseEnrollment.objects.filter(course_id = ss_course_key, 
                                                            user_id =  friend['edX_id'], 
                                                            is_active = True )
                if query_set.count() == 1:
                    fb_friends_in_course.append(friend)


            fb_friends_in_course = {'friends' : fb_friends_in_course}
            return Response(fb_friends_in_course)
        return Response({})

    def get_token(self, request): 
        if 'oauth-token' in request.GET:
            return request.GET['oauth-token']


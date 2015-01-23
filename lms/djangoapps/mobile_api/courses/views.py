"""
Views for courses info API
"""


from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
from courseware.access import is_mobile_available_for_user
from student.models import CourseEnrollment
from social.apps.django_app.default.models import UserSocialAuth
from mobile_api.users.serializers import CourseEnrollmentSerializer
from openedx.core.djangoapps.user_api.api.profile import preference_info
import facebook
import json
import urllib2

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
    # TODO: serializer?


    def list(self, request, *args, **kwargs):
        # Get all the users FB friends
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

            # Get the linked edX user if it exists
            friends_that_are_edX_users = []
            for friend in data:
                name = friend['name']
                fb_id = friend['id']
                query_set = UserSocialAuth.objects.filter(uid=unicode(fb_id))
                if query_set.count() == 1: 
                    friend['edX_id'] = query_set[0].user_id
                    friends_that_are_edX_users.append(friend)
            
            # Filter based on TOC after merging with TOC branch
            friends_that_are_edX_users_with_sharing = []
            for friend in friends_that_are_edX_users:
                share_pref_setting = preference_info(friend['name'])
                if 'share_pref' in share_pref_setting and share_pref_setting['share_pref'] == 'True':
                    friends_that_are_edX_users_with_sharing.append(friend)

            # For each friend get the courses they are a member of
            # and add them to the result set if they are not in it.
            enrollments = []
            for friend in friends_that_are_edX_users_with_sharing:
                query_set = CourseEnrollment.objects.filter(user_id = friend['edX_id'], 
                                                            is_active = True)
                if query_set.count() > 0:
                    for i in range(len(query_set)):
                        if not self.is_member(enrollments, query_set[i]):
                            enrollments.append(query_set[i])

            courses = [enrollment for enrollment in enrollments if enrollment.course and is_mobile_available_for_user(self.request.user, enrollment.course)]

            serialized_courses = CourseEnrollmentSerializer(courses)
            return Response(serialized_courses.data)

        # TODO: Error for no oath token
        return Response({})

    def get_token(self, request): 
        if 'oauth-token' in request.GET:
            return request.GET['oauth-token']

    def is_member(self, enrollments, query_set_item):
        ''' 
            Return true if the query_set_item is in enrollments
        '''
        for enrollment in enrollments:
            if query_set_item.course_id == enrollment.course_id:
                return True
        return False

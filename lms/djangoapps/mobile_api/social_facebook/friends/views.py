"""
Views for friends info API
"""

from rest_framework import generics, status
from rest_framework.response import Response
from openedx.core.djangoapps.user_api.api.profile import preference_info
from opaque_keys.edx.keys import CourseKey
from student.models import CourseEnrollment
from ...utils import mobile_view
from ..utils import get_friends_from_facebook, get_linked_edx_accounts
from lms.djangoapps.mobile_api.social_facebook.friends import serializers
from django.conf import settings

_FACEBOOK_API_VERSION = settings.FACEBOOK_API_VERSION


@mobile_view()
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
    serializer_class = serializers.FriendsInCourseSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET, files=request.FILES)
        if serializer.is_valid():
            # Get all the users FB friends
            data = get_friends_from_facebook(serializer)
            if type(data) != list and data.status_code == 400:
                return data
            # For each friend check if they are a linked edX user
            friends_that_are_linkend_edX_users = get_linked_edx_accounts(data)
            # Filter by sharing preferences
            friends_that_are_edX_users_with_sharing = [friend for friend in friends_that_are_linkend_edX_users if self.sharing_pref_true(friend)]
            course_key = CourseKey.from_string(kwargs['course_id'])
            fb_friends_in_course = [friend for friend in friends_that_are_edX_users_with_sharing if self.is_member(course_key, friend)]
            return Response({'friends': fb_friends_in_course})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_member(self, course_key, friend):
            return CourseEnrollment.objects.filter(course_id=course_key,
                                                        user_id=friend['edX_id'], 
                                                        is_active=True).count() == 1

    def sharing_pref_true(self, friend):
        share_pref_setting = preference_info(friend['edX_username'])
        return ('share_pref' in share_pref_setting) and (share_pref_setting['share_pref'] == 'True')

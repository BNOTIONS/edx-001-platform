"""
Views for courses info API
"""


from rest_framework import generics, status
from rest_framework.response import Response
from courseware.access import is_mobile_available_for_user
from student.models import CourseEnrollment
from mobile_api.users.serializers import CourseEnrollmentSerializer
from openedx.core.djangoapps.user_api.api.profile import preference_info
from ...utils import mobile_view
from ..utils import get_friends_from_facebook, get_linked_edx_accounts
from lms.djangoapps.mobile_api.social_facebook.courses import serializers
from django.conf import settings

_FACEBOOK_API_VERSION = settings.FACEBOOK_API_VERSION


@mobile_view()
class CoursesWithFriends(generics.ListAPIView):
    """
    **Use Case**

        API endpoint for retriving all the courses that a users friends are in.
        Note that only friends that allow their courses to be shared will be included.

    **Example request**

        GET /api/mobile/v0.5/courses/friends

    **Response Values**

        See UserCourseEnrollmentsList in lms/djangoapps/mobile_api/users for the structure of the response values.
    """
    serializer_class = serializers.CoursesWithFriendsSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET, files=request.FILES)
        if serializer.is_valid():
            # Get friends from Facebook
            data = get_friends_from_facebook(serializer)
            if type(data) != list and data.status_code == 400:
                return data
            friends_that_are_linkend_edx_users = get_linked_edx_accounts(data)
            # Filter by sharing preferences
            friends_that_are_edx_users_with_sharing = [friend for friend in friends_that_are_linkend_edx_users
                                if self.sharing_pref_true(friend)]
            # Get unique courses
            enrollments = self.get_unique_courses(friends_that_are_edx_users_with_sharing)
            # Get course objects 
            courses = [enrollment for enrollment in enrollments if enrollment.course
                                and is_mobile_available_for_user(self.request.user, enrollment.course)]
            return Response(CourseEnrollmentSerializer(courses, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_unique_courses(self, friends_that_are_edX_users_with_sharing):
        '''
            Return a list of unique courses friends_that_are_edX_users_with_sharing are in
        '''
        enrollments = []
        for friend in friends_that_are_edX_users_with_sharing:
            query_set = CourseEnrollment.objects.filter(user_id=friend['edX_id'], is_active=True).exclude(course_id__in=[enrollment.course_id for enrollment in enrollments])
            if query_set.count() > 0:
                for i in range(len(query_set)):
                    enrollments.append(query_set[i])
        return enrollments

    def is_member(self, enrollments, query_set_item):
        ''' 
            Return true if the query_set_item is in enrollments
        '''
        for enrollment in enrollments:
            if query_set_item.course_id == enrollment.course_id:
                return True
        return False

    def sharing_pref_true(self, friend):
        share_pref_setting = preference_info(friend['edX_username'])
        return ('share_pref' in share_pref_setting) and (share_pref_setting['share_pref'] == 'True')

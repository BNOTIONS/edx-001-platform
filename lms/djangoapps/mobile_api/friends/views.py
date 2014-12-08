"""
Views for course info API
"""
from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response

from courseware.courses import get_course_about_section, get_course_info_section_module
from opaque_keys.edx.keys import CourseKey

from xmodule.modulestore.django import modulestore


class CourseWithFriends(generics.ListAPIView):
    """
    **Use Case**

        TODO

    **Example request**:

        TODO

    **Response Values**

        TODO
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response({"hey" : "you"})


class FriendsCourses(generics.ListAPIView):
    """
    **Use Case**

        TODO

    **Example request**:

        TODO

    **Response Values**

        TODO
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response({"hey" : "you"})


class FriendsGroups(generics.ListAPIView):
    """
    **Use Case**

        TODO

    **Example request**:

        TODO

    **Response Values**

        TODO
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response({"hey" : "you"})

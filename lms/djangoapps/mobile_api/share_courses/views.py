"""
Views for course info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response



class ShareCourses(generics.CreateAPIView):
    """
    **Use Case**

        An API to set toggle for sharing a users course info publicly

    **Example request**:

        TODO

    **Response Values**

        TODO
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        boolean = request.POST['share_courses']
        return Response(
            {"share_courses": boolean}
        )

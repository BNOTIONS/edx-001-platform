"""
Views for users sharing preferences
"""

from rest_framework import generics, permissions, status 
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
import serializers

from user_api.api.profile import preference_info, update_preferences

from nose.tools import set_trace

class UserSharing(generics.ListCreateAPIView):
    """
    **Use Case**


    **Example request**:

        GET /api/mobile/v0.5/

    **Response Values**

        {'share_pref': 'true'}

    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSharingSerializar


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            value = serializer.object['share_pref']
            try:
                update_preferences(request.user.username, share_pref=value)
            except Exception, e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=e.data)
            return Response(preference_info(request.user.username))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs): 
        return Response(preference_info(request.user.username))



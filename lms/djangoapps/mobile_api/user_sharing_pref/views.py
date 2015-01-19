"""
Views for users sharing preferences
"""

from rest_framework import generics, permissions, status 
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
from user_api.api.profile import preference_info, update_preferences
import serializers


class UserSharing(generics.ListCreateAPIView):
    """
    **Use Case**

        An API to retrieve or update the users social sharing settings

    **GET Example request**:

        GET /api/mobile/v0.5/settings/share_pref/ 

    **GET Response Values**

        {'share_pref': 'True'}

    **POST Example request**:

        POST /api/mobile/v0.5/settings/share_pref/

        paramters: share_pref : True 

    **POST Response Values**

        {'share_pref': 'True'}

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



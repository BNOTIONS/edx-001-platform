"""
Views for users sharing preferences
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response


# from user_api.models import UserPreference
# from django.contrib.auth.models import User
from user_api.api.profile import * 

from nose.tools import set_trace

class UserSharing(generics.CreateAPIView):
    """
    **Use Case**


    **Example request**:

        GET /api/mobile/v0.5/

    **Response Values**

        {'share_pref': 'true'}

    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # set_trace()
        try: 
            value = request.POST['share_pref']
            update_preferences(request.user.username, share_pref=value)
        except Exception, e: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.data)

        return Response(preference_info(request.user.username))



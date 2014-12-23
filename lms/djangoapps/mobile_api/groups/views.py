"""
Views for groups info API
"""

from rest_framework import generics, permissions, status
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response

import httplib2
import urllib 
import facebook     # TODO: talk to lee about dependencies.



# TODO: don't leave this here. 
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"

from nose.tools import set_trace


class GroupsCreate(generics.CreateAPIView):
    """
    **Use Case**

        An API to create new course groups

    **Example request**:

        POST /api/mobile/v0.5/groups/create

        Paramters:  name : string, 
                    description : string, 
                    privacy : open/closed

    **Response Values**

        {"group-id": group_id}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
        url = "/v2.2/" + _APP_ID + "/groups"
        
        post_args = {}
        for key in request.POST.keys(): 
            post_args[key] = request.POST[key]
        try:
            app_groups_response = graph.request(url, post_args=post_args)
        except Exception, e:
            return Response({'error' : e.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(app_groups_response)



class GroupsInvite(generics.CreateAPIView):
    """
    **Use Case**

        An API to invite members to a group

    **Example request**:

        POST /groups/invite/<group-id>/members


    **Response Values**

        {"success": "true"}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        member_ids = request.POST['member-ids']
        oauth_token = request.POST['oauth-token']
        return Response(
            {"success": "true"}
        )


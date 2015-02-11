"""
Views for groups info API
"""

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from ...utils import mobile_view
from lms.djangoapps.mobile_api.social_facebook.groups import serializers
import facebook

from django.conf import settings
_FACEBOOK_API_VERSION = settings.FACEBOOK_API_VERSION
_FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
_FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET

@mobile_view()
class Groups(generics.CreateAPIView, mixins.DestroyModelMixin):
    """
    **Use Case**

        An API to Create or Delete course groups.

    **Creation Example request**:

        POST /api/mobile/v0.5/social/facebook/groups/

        Parameters: name : string,
                    description : string, 
                    privacy : open/closed

    **Creation Response Values**

        {"id": group_id}


    **Deletion Example request**:

        DELETE /api/mobile/v0.5/social/facebook/groups/<group_id>

    **Deletion Response Values**

        {"success" : "true"}

    """
    serializer_class = serializers.GroupSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            try:
                # from nose.tools import set_trace
                # set_trace()
           
                post_args = request.POST.dict()
                graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
                app_groups_response = graph.request(_FACEBOOK_API_VERSION + '/' + _FACEBOOK_APP_ID + "/groups", post_args=post_args)
                return Response(app_groups_response)
            except facebook.GraphAPIError, ex:
                return Response({'error': ex.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
            post_args = {'method': 'delete'}
            return Response(graph.request(_FACEBOOK_API_VERSION + '/' + _FACEBOOK_APP_ID + "/groups/" + kwargs['group_id'], post_args=post_args))
        except facebook.GraphAPIError, ex:
            return Response({'error': ex.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)


@mobile_view()
class GroupsMembers(generics.CreateAPIView, mixins.DestroyModelMixin):
    """
    **Use Case**

        An API to Invite and Remove members to a group

    **Invite Example request**:

        POST /api/mobile/v0.5/social/facebook/groups/<group_id>/member/

        Parameters: members : int,int,int... 


    **Invite Response Values**

        {"member_id" : success/error_message}       A response with each member_id and whether or not
                                                    the member was added successfully. If the member was 
                                                    not added successfully the Facebook error message is provided. 
        
    **Remove Example request**:

        DELETE /api/mobile/v0.5/social/facebook/groups/<group_id>/member/<member_id>

    **Remove Response Values**

        {"success" : "true"}                                    
    """
    serializer_class = serializers.GroupsMembersSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
            url = _FACEBOOK_API_VERSION + '/' + kwargs['group_id'] + "/members"
            member_ids = serializer.object['member_ids'].split(',')                        
            response = {}
            for member_id in member_ids:
                try:
                    if 'success' in graph.request(url, post_args={'member' : member_id}): 
                        response[member_id] = 'success'
                except facebook.GraphAPIError, ex:
                    response[member_id] = ex.result['error']['message']
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
            post_args = {'method': 'delete', 'member': kwargs['member_id']}
            return Response(graph.request(_FACEBOOK_API_VERSION + '/' + kwargs['group_id'] + "/members", post_args=post_args))
        except facebook.GraphAPIError, ex:
            return Response({'error': ex.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)

"""
Views for groups info API
"""

from rest_framework import generics, permissions, status, mixins
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
from ..settings import FB_SETTINGS
import serializers
import facebook

# TODO: change this to final config
from ..settings import FB_SETTINGS
_FACEBOOK_APP_ID = FB_SETTINGS['_FACEBOOK_APP_ID']
_FACEBOOK_APP_SECRET = FB_SETTINGS['_FACEBOOK_APP_SECRET']
_FACEBOOK_API_VERSION = FB_SETTINGS['_FACEBOOK_API_VERSION']


class Groups(generics.CreateAPIView, mixins.DestroyModelMixin):
    """
    **Use Case**

        An API to Create or Delete course groups.

    **Creation Example request**:

        POST /api/mobile/v0.5/create/<group_id>

        Parameters:  name : string, 
                    description : string, 
                    privacy : open/closed

    **Creation Response Values**

        {"group-id": group_id}
    

    **Deletion Example request**:
        
        DELETE /api/mobile/v0.5/create/<group_id>

    **Deletion Response Values**

        {"success" : "true"}

    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GroupSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            post_args = {}
            for key in request.POST.keys(): 
                post_args[key] = request.POST[key]
            try:
                graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
                app_groups_response = graph.request(_FACEBOOK_API_VERSION + _FACEBOOK_APP_ID + "/groups", post_args=post_args)
            except Exception, e:
                return Response({'error' : e.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)

            return Response(app_groups_response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        if 'group_id' in kwargs:
            post_args = {'method' : 'delete'}
            graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID], _FACEBOOK_APP_SECRET))
            result = graph.request(_FACEBOOK_API_VERSION + _FACEBOOK_APP_ID + "/groups/" + kwargs['group_id'], post_args=post_args)
            return Response(result)
        else:
            return Response({'error' : 'Missing group id'}, status=status.HTTP_400_BAD_REQUEST)



class GroupsMembers(generics.CreateAPIView, mixins.DestroyModelMixin):
    """
    **Use Case**

        An API to Invite and Remove members to a group

    **Invite Example request**:

        POST /api/mobile/v0.5/member/<group_id>/

        Parameters: members : int,int,int... 


    **Invite Response Values**

        {"member_id" : success/error_message}       A response with each member_id and whether or not
                                                    the member was added successfully. If the member was 
                                                    not added successfully the Facebook error message is provided. 
        
    **Remove Example request**:

        DELETE /api/mobile/v0.5/member/<group_id>/<member_id>

    **Remove Response Values**

        {"success" : "true"}                                    
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GroupsMembersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
            if 'group_id' in kwargs: 
                url = _FACEBOOK_API_VERSION + kwargs['group_id'] + "/members"
            member_ids = serializer.object['member_ids'].split(',')                        
            response = {}
            contains_error = False
            for member_id in member_ids:
                try:
                    if 'success' in graph.request(url, post_args={'member' : member_id}): 
                        response[member_id] = 'success'
                except Exception, e:
                    from nose.tools import set_trace
                    set_trace()
                    response[member_id] = e.result['error']['message']
                    contains_error = True

            status_code = status.HTTP_201_CREATED if contains_error else status.HTTP_200_OK
            return Response(response, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if 'member_id' in kwargs and 'group_id' in kwargs:
            graph = facebook.GraphAPI(facebook.get_app_access_token(_FACEBOOK_APP_ID, _FACEBOOK_APP_SECRET))
            post_args = {'method' : 'delete', 'member' : kwargs['member_id']}
            url = _FACEBOOK_API_VERSION + kwargs['group_id'] + "/members" 
            result = graph.request(url, post_args=post_args)
            return Response(result)
        if 'member_id' not in kwargs: 
            return Response({'error' : 'Missing member id'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({'error' : 'Missing group id'}, status=status.HTTP_400_BAD_REQUEST)

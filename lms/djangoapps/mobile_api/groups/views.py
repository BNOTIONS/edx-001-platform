"""
Views for groups info API
"""

from rest_framework import generics, permissions, status, mixins
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response
import serializers
# TODO: dependencies to be added to the vagrant 
import facebook     

# TODO: This should not be in the final commit
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"

_FACEBOOK_API_VERSION = "/v2.2/"


class Groups(generics.CreateAPIView, mixins.DestroyModelMixin):
    """
    **Use Case**

        An API to Create or Delete course groups.

    **Creation Example request**:

        POST /api/mobile/v0.5/create/<group_id>

        Paramters:  name : string, 
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
            graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
            url = _FACEBOOK_API_VERSION + _APP_ID + "/groups"
            
            post_args = {}
            for key in request.POST.keys(): 
                post_args[key] = request.POST[key]
            try:
                app_groups_response = graph.request(url, post_args=post_args)
            except Exception, e:
                return Response({'error' : e.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)
            return Response(app_groups_response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        if 'group_id' in kwargs:
            graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
            post_args = {'method' : 'delete'}
            url = _FACEBOOK_API_VERSION + _APP_ID + "/groups/" + kwargs['group_id']
            result = graph.request(url, post_args=post_args)
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

        {"success" : "true"}        If adding all the member succeeded.
        
        {"error" : "error message", 
         "member" : "id"}           If one of the members provided can't be added to the group. 
                                    The error message pertains to the first member that couldn't be added.
                                    Note that either all the memebers are added or none at all. 

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
            graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
            if 'group_id' in kwargs: 
                url = _FACEBOOK_API_VERSION + kwargs['group_id'] + "/members"
            else: 
                return Response({'error' : 'Missing group id'}, status=status.HTTP_400_BAD_REQUEST)

            if 'member_ids' in request.POST:
                member_ids = request.POST['member_ids'].split(',')
                successful_additions = []
                for member_id in member_ids:
                    post_args = {'member' : member_id}
                    try:
                        response = graph.request(url, post_args=post_args)
                        if 'success' in response: 
                            successful_additions.append(member_id)
                    except Exception, e:
                        for member_to_remove in successful_additions:
                            post_args = {'member' : member_to_remove, 'method' : 'delete'}
                            graph.request(url, post_args=post_args) 
                        return Response({'error' : e.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success" : "true"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if 'member_id' in kwargs and 'group_id' in kwargs:
            graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
            post_args = {'method' : 'delete', 'member' : kwargs['member_id']}
            url = _FACEBOOK_API_VERSION + kwargs['group_id'] + "/members" 
            result = graph.request(url, post_args=post_args)
            return Response(result)
        if 'member_id' not in kwargs: 
            return Response({'error' : 'Missing member id'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({'error' : 'Missing group id'}, status=status.HTTP_400_BAD_REQUEST)

"""
Views for groups info API
"""

from rest_framework import generics, permissions, status
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response

import facebook     # TODO: dependencies to be added to the vagrant 



# TODO: This should not be in the final commit
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"

_FACEBOOK_API_VERSION = "/v2.2/"
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
        url = _FACEBOOK_API_VERSION + _APP_ID + "/groups"
        
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

        Parameters: members : int,int,int... 


    **Response Values**

        {"success" : "true"}        If adding all the member succeeded.
        
        {"error" : "error message", 
         "member" : "id"}           If one of the members provided can't be added to the group. 
                                    The error message pertains to the first member that couldn't be added.
                                    Note that either all the memebers are added or none at all. 
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
        if 'group_id' in kwargs: 
            url = _FACEBOOK_API_VERSION + kwargs['group_id'] + "/members"
        else: 
            return Response({'error' : 'Missing group id'}, status=status.HTTP_400_BAD_REQUEST)

        if 'member-ids' in request.POST:
            member_ids = request.POST['member-ids'].split(',')
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


class GroupsDelete(generics.DestroyAPIView):
    """
    **Use Case**

        An API to delete a group

    **Example request**:

        DELETE /groups/<group-id>

    **Response Values**

        {"success" : "true"}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
        post_args = {'method' : 'delete'}
        url = _FACEBOOK_API_VERSION + _APP_ID + "/groups/" + kwargs['group_id']
        result = graph.request(url, post_args=post_args)
        return Response(result)


class GroupsRemoveMember(generics.DestroyAPIView):
    """
    **Use Case**

        An API to remove a group member form a group

    **Example request**:

        DELETE /remove/<group-id>/member/<member-id>

    **Response Values**

        {"success" : "true"}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        graph = facebook.GraphAPI(facebook.get_app_access_token(_APP_ID, _APP_SECRET))
        post_args = {'method' : 'delete', 'member' : kwargs['member_id']}
        url = _FACEBOOK_API_VERSION + kwargs['group_id'] + "/members" 
        result = graph.request(url, post_args=post_args)
        return Response(result)




"""
Views for groups info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response

import httplib2
import urllib 
import facebook     # TODO: talk to lee about dependencies.
from nose.tools import set_trace

# TODO: don't leave this in here
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"
_BASE_URL = "https://graph.facebook.com"

class Groups(generics.RetrieveAPIView):
    """
    **Use Case**

        An API to support retrival of all the groups related to the edX app that the user is in. 

    **Example request**:

        GET /api/mobile/v0.5/groups

    **Response Values**

        {"groups": [ {  "id": "912988378712053", 
                            "owner": {  "id": "10154805434030300", 
                                        "name": "Daniel Eidan"
                                        }, 
                            "name": "edX public test1", 
                            "venue": { "street": ""
                                        }, 
                            "privacy": "OPEN", 
                            "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y1/r/vF2XT-TEoHq.png", 
                            "updated_time": "2014-12-03T20:38:32+0000", 
                            "email": "912988378712053@groups.facebook.com"
                        } ... 
                        ]
            }
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Get all the groups associated with the app /734266930001243/groups
        # Get all the user /me/groups
        # The intersection of these is the desired response
        
        # TODO: pass this in as a param 
        oauth_access_token = "CAAKbz9eIdVsBAJ9B7ZCb8wSrB7KUOvhLHpe3BPZBfL6irMwDgSXA7fZCAmpVg2qsTZCbuX5OZBOdqtKiGakPjR9Tk0bsOeS7uzyU0hzg1xNbne64qoP2dJ7G42apxLsH5A1QZC6Kxav3tWDmJbvd4V5RqDi1noZB8JNwoFtW2mIi2ew6ffoXSAjG672zXlCzfZABZAx8fRsC7S8CxnMXtZAcA7"
        graph = facebook.GraphAPI(oauth_access_token)
        
        url_user_groups = "/v2.2/me/groups"
        user_groups_response = graph.request(url_user_groups)

        graph.api_key = facebook.get_app_access_token(_APP_ID, _APP_SECRET)
        url_app_groups = "/v2.2/" + _APP_ID + "/groups"
        app_groups_response = graph.request(url_app_groups)
        
        # TODO error checking for valid responses
        return Response({"groups": get_intersection_groups(user_groups_response['data'], app_groups_response['data'])})


        # return Response(
        #     {"groups": [ {  "id": "912988378712053", 
        #                     "owner": {  "id": "10154805434030300", 
        #                                 "name": "Daniel Eidan"
        #                                 }, 
        #                     "name": "edX public test1", 
        #                     "venue": { "street": ""
        #                                 }, 
        #                     "privacy": "OPEN", 
        #                     "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y1/r/vF2XT-TEoHq.png", 
        #                     "updated_time": "2014-12-03T20:38:32+0000", 
        #                     "email": "912988378712053@groups.facebook.com"
        #                 }
        #                 ]
        #     }
        # )

def get_intersection_groups(set1, set2): 
    """ 
    """
    # TODO make this fuckin efficient 
    # set_trace()
    result_list = []
    for obj1 in set1: 
        for obj2 in set2:
            if obj1['id'] == obj2['id']: 
                result_list.append(obj1)
    # set_trace()
    return result_list


class GroupsCreate(generics.CreateAPIView):
    """
    **Use Case**

        An API to create new course groups

    **Example request**:

        POST /api/mobile/v0.5/groups/create

    **Response Values**

        {"group-id": group_id}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        group_id = request.POST['group-id']
        return Response(
            {"group-id": group_id}
        )



class GroupsInvite(generics.CreateAPIView):
    """
    **Use Case**

        An API to invite members to a group

    **Example request**:

        POST /groups/invite/<group-id>/members


    **Response Values**

        {"member": member}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        member = request.POST['member']
        return Response(
            {"member": member}
        )

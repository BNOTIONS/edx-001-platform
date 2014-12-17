"""
Views for groups info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response


# TODO: don't leave this here. 
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"

from nose.tools import set_trace

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
        # To get all groups associated with the app /734266930001243/groups
        # To get all the user /me/groups
        # The intersection of these is the desired response
        oauth_token = request.GET['oauth-token']
        return Response(
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
                        }
                        ]
            }
        )



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
        name = request.POST['name']
        description = request.POST['description']
        privacy = request.POST['privacy']
        admin_id = request.POST['admin-id']
        oauth_token = request.POST['oauth-token']
        return Response({'name' : name,
                        'description' : description,
                        'privacy' : privacy,
                        'admin-id' : admin_id,
                        'oauth-token' : oauth_token
                        })



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

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

# TODO: don't leave this here. 
_APP_SECRET = "8a982cfdc0922c9fe57bd63edab6b62f"
_APP_ID = "734266930001243"
_BASE_URL = "https://graph.facebook.com"

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
        # Get all the groups associated with the app /734266930001243/groups
        # Get all the user /me/groups
        # The intersection of these is the desired response
        
        set_trace()

        # TODO: pass this in as a param 
        oauth_access_token = "CAACEdEose0cBAMh8IJXYlonj1ZCzvKwCv6v7rKdYlV164ezcuHAqZCig11OlQPRZCvFhG3aBGb78IKIeIhXC1UIZA3DJyNIZCHIZBWNAhF2ymleGNZB92Li4yIO1V19rMZBY3JjbVeIRuAsyzg97hYLi1jJAy4uwjsGG0J2mlCTYtpq9K7nup0xsUpcfIGyco6DxtZBM0BZBNHNtA9sfrfrXwB"
        graph = facebook.GraphAPI(oauth_access_token)
        
        url_user_groups = "/v2.2/me/groups"
        user_groups_response = graph.request(url_user_groups)

        graph.api_key = facebook.get_app_access_token(_APP_ID, _APP_SECRET)
        url_app_groups = "/v2.2/" + _APP_ID + "/groups"
        app_groups_response = graph.request(url_app_groups)
        
        # TODO error checking for valid responses
        return Response({"groups": get_intersection_groups(user_groups_response['data'], app_groups_response['data'])})

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
        name = request.POST['name']
        description = request.POST['description']
        privacy = request.POST['privacy']
        admin_id = request.POST['admin-id']
        oauth_token = request.POST['oauth-token']
        return Response({"group-id": '12345'})



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


class GroupsMembers(generics.RetrieveAPIView): 
    """
    **Use Case**

        An API to retrive all members of a group

    **Example request**:

        GET /groups/<group-id>/members


    **Response Values**

        {   "members":
                [{
                    "name": "test",
                    "id": "12345",
                },
                ...
                ]
        }
    """    
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # set_trace()
        return Response({"members": 
                            [{  "name": "Daniel Eidan",
                                "id": "10154831816670300"},
                            {   "name": "Marc Ashman", 
                                "id": "10154833899435243"},
                            {   "name": "Peter Organa", 
                                "id": "10154805420820176"},
                            {   "name": "Joey Freund", 
                                "id": "1279985874"}, 
                            {   "name": "Yin Zhuoqun", 
                                "id": "1600206076"},    
                            {   "name": "David Liu", 
                                "id": "1658520223"},
                            {   "name": "Andrew Joe", 
                                "id": "120401174"}, 
                            {   "name": "Gaelan D'costa", 
                                "id": "122600141"}, 
                            {   "name": "Hafiz Vellani", 
                                "id": "122609084"}, 
                            {   "name": "Adir Krafman", 
                                "id": "500301193"}, 
                            {   "name": "Naeem Lakhani", 
                                "id": "502193756"}, 
                            {   "name": "Alex Mann", 
                                "id": "502576321"}, 
                            {   "name": "Natasha Dalal", 
                                "id": "506753913"}, 
                            {   "name": "Adam Borzecki", 
                                "id": "507174319"}, 
                            {   "name": "Bryant Balatbat", 
                                "id": "512414329"}, 
                            {   "name": "Nahim Nasser", 
                                "id": "516528519"}, 
                            {   "name": "Farzana Nasser", 
                                "id": "572710051"}, 
                            {   "name": "Aaron Ritchie", 
                                "id": "578710450"}, 
                            {   "name": "Karthik Ramakrishnan", 
                                "id": "584467742"}, 
                            {   "name": "Sinai Gross", 
                                "id": "591867536"}, 
                            {   "name": "Ani Tumanyan", 
                                "id": "617573112"}, 
                            {   "name": "Paul Jeffrey Crowe", 
                                "id": "635195067"}, 
                            {   "name": "Eitan Cohen", 
                                "id": "657887138"}, 
                            {   "name": "Eli Atlas", 
                                "id": "674674636"}, 
                            {   "name": "Mark Reale", 
                                "id": "676480219"}]
                })







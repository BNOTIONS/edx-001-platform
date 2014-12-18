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
                        }, 
                        {
                          "id": "753283111432958", 
                          "name": "Bnauts", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "OPEN", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-12-17T19:36:33+0000", 
                          "email": "753283111432958@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        }, 
                        {
                          "id": "734295443331725", 
                          "name": "devA_groupA", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-12-11T22:53:03+0000", 
                          "email": "734295443331725@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        }, 
                        {
                          "id": "734297203331549", 
                          "name": "devA_groupB", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-11T19:48:43+0000", 
                          "email": "734297203331549@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        }, 
                        {
                          "id": "734297936664809", 
                          "name": "devA_groupc", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-11T19:50:42+0000", 
                          "email": "734297936664809@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        },
                        {
                          "id": "734693669958569", 
                          "name": "testmesh", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "OPEN", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-12T20:29:26+0000", 
                          "email": "734693669958569@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        }, 
                        {
                          "id": "734713993289870", 
                          "name": "weirdtest", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-12T20:29:31+0000", 
                          "email": "734713993289870@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        },
                        {
                          "id": "734805136614089", 
                          "name": "test123", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-12T20:31:54+0000", 
                          "email": "734805136614089@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        },
                        {
                          "id": "735235816571021", 
                          "name": "dumbpotatosonly", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-13T17:09:42+0000", 
                          "email": "735235816571021@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
                        }, 
                        {
                          "id": "735277569900179", 
                          "name": "supercooltestgroup?admin", 
                          "venue": {
                            "street": ""
                          }, 
                          "privacy": "CLOSED", 
                          "icon": "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y0/r/XCrOg4YmGg4.png", 
                          "updated_time": "2014-11-13T18:59:00+0000", 
                          "email": "735277569900179@groups.facebook.com", 
                          "parent": {
                            "name": "edX_bnotion_devA", 
                            "namespace": "edxbnotionsns", 
                            "id": "734266930001243"
                          }
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







"""
Views for course info API
"""

# TODO go over imports 
from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response

from courseware.courses import get_course_about_section, get_course_info_section_module
from opaque_keys.edx.keys import CourseKey

from xmodule.modulestore.django import modulestore


class Groups(generics.RetrieveAPIView):
    """
    **Use Case**

        An API to support retrival of all the groups related to the edX app

    **Example request**:

        GET /api/mobile/v0.5/groups/

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

        TODO

    **Response Values**

        TODO
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        group_id = request.POST['group-id']
        # TODO: Change this to actually make the group
        return Response(
            {"group-id": group_id}
        )

"""
Views for friends info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response

from nose.tools import set_trace

class FriendsInCourse(generics.ListAPIView):
    """
    **Use Case**

        API endpoint that returns all the users friends that are in the course specified.
        Note that only friends that allow their courses to be shared will be included.

    **Example request**:

        GET /api/mobile/v0.5/friends/course/<course_id>

        where course_id is in the form of /edX/DemoX/Demo_Course

    **Response Values**

        {   "friends":
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

    def list(self, request, *args, **kwargs):
        return Response(
            {"friends": [{  "name": "Daniel Eidan",
                            "id": "10154831816670300"},
                        {   "name": "Marc Ashman", 
                            "id": "10154833899435243"},
                        {   "name": "Peter Organa", 
                            "id": "10154805420820176"}
                        ]
            }
        )



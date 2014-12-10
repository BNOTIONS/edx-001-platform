"""
Views for friends info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response


class FriendsInCourse(generics.ListAPIView):
    """
    **Use Case**

        API endpoint that returns all the users friends that are in the course specified.
        Note that only friends that allow their courses to be shared will be included.

    **Example request**:

        GET /api/mobile/v0.5/friends/course/<course-id>

    **Response Values**

        {   "friends":
                [{
                    "name": "test",
                    "id": "12345",
                    "data": {
                        "is_silhouette": "False",
                        "url": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c0.0.50.50/p50x50/10646821_10154623368965300_489101526887946617_n.jpg?oh=d568412c06a929dff150b5d507c63c4c&oe=5546DAF3&__gda__=1427107330_10f1d3e5e0d2f4d9c1fd7dbb0d6a4652"
                    }
                },
                ...
                ]
            }
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(
            {"friends": [{
                    "name": "test",
                    "id": "12345",
                    "data": {
                        "is_silhouette": "False",
                        "url": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c0.0.50.50/p50x50/10646821_10154623368965300_489101526887946617_n.jpg?oh=d568412c06a929dff150b5d507c63c4c&oe=5546DAF3&__gda__=1427107330_10f1d3e5e0d2f4d9c1fd7dbb0d6a4652"
                    }
                }]
            }
        )



class FriendsInGroup(generics.ListAPIView):
    """
    **Use Case**

        API endpoint that returns all the users friends that are in the group specified. 
        Note that only friends that allow their courses to be shared will be included.


    **Example request**

        GET /api/mobile/v0.5/friends/group/<group-id>

    **Response Values**

        {   "friends":
                [{
                    "name": "test",
                    "id": "12345",
                    "data": {
                        "is_silhouette": "False",
                        "url": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c0.0.50.50/p50x50/10646821_10154623368965300_489101526887946617_n.jpg?oh=d568412c06a929dff150b5d507c63c4c&oe=5546DAF3&__gda__=1427107330_10f1d3e5e0d2f4d9c1fd7dbb0d6a4652"
                    }
                },
                ...
                ]
            }
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(
            {"friends": [{
                    "name": "test",
                    "id": "12345",
                    "data": {
                        "is_silhouette": "False",
                        "url": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c0.0.50.50/p50x50/10646821_10154623368965300_489101526887946617_n.jpg?oh=d568412c06a929dff150b5d507c63c4c&oe=5546DAF3&__gda__=1427107330_10f1d3e5e0d2f4d9c1fd7dbb0d6a4652"
                    }
                }]
            }
        )

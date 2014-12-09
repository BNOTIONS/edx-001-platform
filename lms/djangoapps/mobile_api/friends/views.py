"""
Views for course info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response


class CoursesWithFriends(generics.ListAPIView):
    """
    **Use Case**

        API endpoint for retriving all the courses that a users friends are in. 
        Note that only friends that allow their courses to be shared will be included.

    **Example request**

        GET /api/mobile/v0.5/friends

    **Response Values**

        {"courses": [
            {   "created": "2014-12-09 16:58:31.926438",
            "mode": "honor",
            "is_active": "True",
            "course": {
                "course_about": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/about",
                "course_updates": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/updates",
                "number": "course_4",
                "org": "org.4",
                "video_outline": "http://testserver/api/mobile/v0.5/video_outlines/courses/org.4/course_4/Run_4",
                "id": "org.4/course_4/Run_4",
                "latest_updates": {
                    "video": "None"
                },
                "end": "None",
                "name": "Run 4",
                "course_handouts": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/handouts",
                "start": "2030-01-01 00:00:00",
                "course_image": "/c4x/org.4/course_4/asset/images_course_image.jpg"
                }
            },
            ...
        ]}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(
            {"courses": [
                {   "created": "2014-12-09 16:58:31.926438",
                    "mode": "honor",
                    "is_active": "True",
                    "course": {
                        "course_about": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/about",
                        "course_updates": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/updates",
                        "number": "course_4",
                        "org": "org.4",
                        "video_outline": "http://testserver/api/mobile/v0.5/video_outlines/courses/org.4/course_4/Run_4",
                        "id": "org.4/course_4/Run_4",
                        "latest_updates": {
                            "video": "None"
                        },
                        "end": "None",
                        "name": "Run 4",
                        "course_handouts": "http://testserver/api/mobile/v0.5/course_info/org.4/course_4/Run_4/handouts",
                        "start": "2030-01-01 00:00:00",
                        "course_image": "/c4x/org.4/course_4/asset/images_course_image.jpg"
                    }
                }
            ]}
        )



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

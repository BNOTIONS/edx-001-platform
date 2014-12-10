"""
Views for share_courses info API
"""

from rest_framework import generics, permissions
from rest_framework.authentication import OAuth2Authentication, SessionAuthentication
from rest_framework.response import Response


class ShareCourses(generics.ListCreateAPIView):
    """
    **Use Case**

        An API to set toggle for sharing a users course info publicly

    **Example request**:

        GET /api/mobile/v0.5/share_courses


    **Response Values**

        {"share_courses": boolean}
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        boolean = request.POST['share_courses']
        return Response(
            {"share_courses": boolean}
        )

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


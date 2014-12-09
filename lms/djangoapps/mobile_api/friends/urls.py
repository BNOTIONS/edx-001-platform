"""
URLs for course_info API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import CoursesWithFriends, FriendsInCourse, FriendsInGroup

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^$',
        CoursesWithFriends.as_view(),
        name='courses-with-friends'
    ),
    url(
        r'^course/(?P<course_id>[\d]*)$',   #TODO: look into course formatter
        FriendsInCourse.as_view(),
        name='friends-in-course'
    ),
    url(
        r'^group/(?P<group_id>[\d]*)$',
        FriendsInGroup.as_view(),
        name='friends-in-group'
    ),
)

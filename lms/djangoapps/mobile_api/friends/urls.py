"""
URLs for course_info API
"""
from django.conf.urls import patterns, url
from .views import FriendsInCourse, FriendsInGroup

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^course/(?P<course_id>[\d]*)$',
        FriendsInCourse.as_view(),
        name='friends-in-course'
    ),
    url(
        r'^group/(?P<group_id>[\d]*)$',
        FriendsInGroup.as_view(),
        name='friends-in-group'
    ),
)

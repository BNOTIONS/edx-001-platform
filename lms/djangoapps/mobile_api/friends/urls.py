"""
URLs for course_info API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import CourseAboutDetail, CourseUpdatesList, CourseHandoutsList

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^$',
        CourseWithFriends.as_view(),
        name='course-withfriends'
    ),
    url(
        r'^course$',
        FriendsCourses.as_view(),
        name='friends-courses'
    ),
    url(
        r'^groups$',
        FriendsGroups.as_view(),
        name='friends-groups'
    ),
)

"""
URLs for courses API
"""
from django.conf.urls import patterns, url

from .views import ShareCourses, CoursesWithFriends

urlpatterns = patterns(
    'mobile_api.share_courses.views',
    url(
        r'^share_settings$',
        ShareCourses.as_view(),
        name='share_settings'
    ),
    url(
        r'^friends$',
        CoursesWithFriends.as_view(),
        name='courses-with-friends'
    ),
)

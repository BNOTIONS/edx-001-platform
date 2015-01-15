"""
URLs for friends API
"""
from django.conf.urls import patterns, url
from .views import FriendsInCourse

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^course/(?P<course_id>([\w]+/?)+)$',
        FriendsInCourse.as_view(),
        name='friends-in-course'
        ),
    )

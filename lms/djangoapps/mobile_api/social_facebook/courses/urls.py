"""
URLs for courses API
"""
from django.conf.urls import patterns, url

from .views import CoursesWithFriends

urlpatterns = patterns(
    'mobile_api.courses.views',
    url(
        r'^friends$',
        CoursesWithFriends.as_view(),
        name='courses-with-friends'
    ),
)

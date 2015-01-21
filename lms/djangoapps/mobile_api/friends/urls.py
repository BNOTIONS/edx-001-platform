"""
URLs for friends API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import FriendsInCourse

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        # r'^course/(?P<course_id>(([\w]|\.)+/?)+)$', #TODO: remove this
        r'^course/{}$'.format(settings.COURSE_ID_PATTERN),
        FriendsInCourse.as_view(),
        name='friends-in-course'
        ),
    )

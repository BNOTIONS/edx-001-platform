"""
URLs for course_info API
"""
from django.conf.urls import patterns, url

from .views import ShareCourses

urlpatterns = patterns(
    'mobile_api.share_courses.views',
    url(
        r'^$',
        ShareCourses.as_view(),
        name='share_courses'
    ),
)

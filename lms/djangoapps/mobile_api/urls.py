"""
URLs for mobile API
"""
from django.conf.urls import patterns, url, include

from .users.views import my_user_info

# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^users/', include('mobile_api.users.urls')),
    url(r'^my_user_info', my_user_info),
    url(r'^video_outlines/', include('mobile_api.video_outlines.urls')),
    url(r'^course_info/', include('mobile_api.course_info.urls')),
    url(r'^groups/', include('mobile_api.groups.urls')),
    url(r'^share_courses/', include('mobile_api.share_courses.urls')),
    url(r'^friends/', include('mobile_api.friends.urls')),
)

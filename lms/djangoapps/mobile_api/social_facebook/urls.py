"""
URLs for Social Facebook
"""
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'mobile_api.social_facebook.urls',
    url(r'^courses/', include('mobile_api.social_facebook.courses.urls')),
    url(r'^friends/', include('mobile_api.social_facebook.friends.urls')),
    url(r'^groups/', include('mobile_api.social_facebook.groups.urls')),
)
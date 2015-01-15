"""
URLs for users sharing preferences
"""
from django.conf.urls import patterns, url
from .views import UserSharing

urlpatterns = patterns(
    'mobile_api.user_sharing_pref.views',
    url(
        r'^share_pref/$',
        UserSharing.as_view(),
        name='share_pref'
    ),
)

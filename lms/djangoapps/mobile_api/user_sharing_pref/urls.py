"""
URLs for users sharing preferences
"""
from django.conf.urls import patterns, url
from .views import UserSharing

urlpatterns = patterns(
    'mobile_api.user_sharing_pref.views',
    url(
        r'^$',
        UserSharing.as_view(),
        name='user_sharing'
    ),

)

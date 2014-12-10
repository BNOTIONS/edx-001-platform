"""
URLs for course_info API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import Groups, GroupsCreate, GroupsInvite

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^$',                        
        Groups.as_view(),
        name='get-app-groups'
    ),
    url(
        r'^create/$',
        GroupsCreate.as_view(),               
        name='create-new-group'
    ),
    url(
        r'^invite/(?P<group_id>[\d]*)/members$',
        GroupsInvite.as_view(),               
        name='invite-to-group'
    ),
)

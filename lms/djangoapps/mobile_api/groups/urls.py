"""
URLs for groups API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import GroupsCreate, GroupsInvite, GroupsDelete, GroupsRemoveMember

urlpatterns = patterns(
    'mobile_api.course_info.views',
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
    url(
        r'^delete/(?P<group_id>[\d]*)$',
        GroupsDelete.as_view(),               
        name='delete-group'
    ),
    url(
        r'^remove/(?P<group_id>[\d]*)/member/(?P<member_id>[\d]*)$',
        GroupsRemoveMember.as_view(),               
        name='group-remove-member'
    )
)

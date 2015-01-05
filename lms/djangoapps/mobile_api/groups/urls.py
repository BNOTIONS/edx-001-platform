"""
URLs for groups API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import Groups, GroupsMembers, GroupsRemoveMember

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^create/(?P<group_id>[\d]*)$',
        Groups.as_view(),               
        name='create-delete-group'
    ),
    url(
        r'^invite/(?P<group_id>[\d]*)$',
        GroupsMembers.as_view(),               
        name='invite-to-group'
    ), 
    url(
        r'^remove/(?P<group_id>[\d]*)/member/(?P<member_id>[\d]*)$',
        GroupsRemoveMember.as_view(),               
        name='group-remove-member'
    )
)

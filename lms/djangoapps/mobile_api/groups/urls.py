"""
URLs for groups API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import Groups, GroupsMembers

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^create/(?P<group_id>[\d]*)$',
        Groups.as_view(),               
        name='create-delete-group'
    ),
    url(
        r'^member/(?P<group_id>[\d]*)/(?P<member_id>[\d]*,*)$',
        GroupsMembers.as_view(),
        name='group-remove-member'
    )
)

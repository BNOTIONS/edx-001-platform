"""
URLs for groups API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import Groups, GroupsMembers

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^(?P<group_id>[\d]*)$',
        Groups.as_view(),
        name='create-delete-group'
    ),
    url(
        r'^(?P<group_id>[\d]+)/member/(?P<member_id>[\d]*,*)$',
        GroupsMembers.as_view(),
        name='add-remove-member'
    )
)

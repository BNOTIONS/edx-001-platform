"""
URLs for course_info API
"""
from django.conf.urls import patterns, url
from django.conf import settings

from .views import Groups, GroupsCreate

urlpatterns = patterns(
    'mobile_api.course_info.views',
    url(
        r'^$',                        
        Groups.as_view(),               # retrive all app groups
        name='get-app-groups'
    ),
    url(
        r'^(?P<group_name>[\w]*)/$',        # does this pose any restrictions on what group names can be?
        GroupsCreate.as_view(),               
        name='create-new-group'
    ),
)

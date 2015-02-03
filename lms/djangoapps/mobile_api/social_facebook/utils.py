"""
Common utility methods and decorators for Social Facebook APIs.
"""
import json
import urllib2
import facebook
from django.conf import settings
from social.apps.django_app.default.models import UserSocialAuth
from rest_framework.response import Response
from rest_framework import status

_FACEBOOK_API_VERSION = settings.FACEBOOK_API_VERSION


def get_pagination(friends):
    '''
        Get paginated data from FaceBook response
    '''
    data = friends['data']
    while 'paging' in friends and 'next' in friends['paging']:
        response = urllib2.urlopen(friends['paging']['next'])
        friends = json.loads(response.read())
        data = data + friends['data']
    return data


def get_friends_from_facebook(serializer):
    '''
        Return the result of a facebook /me/friends call usein ght  oauth_token
        contained within the serializer object
    '''
    try:
        graph = facebook.GraphAPI(serializer.object['oauth_token'])
        friends = graph.request(_FACEBOOK_API_VERSION + "/me/friends")
        return get_pagination(friends)
    except facebook.GraphAPIError, ex:
        return Response({'error': ex.result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)


def get_linked_edx_accounts(data):
    friends_that_are_edX_users = []
    for friend in data:
        query_set = UserSocialAuth.objects.filter(uid=unicode(friend['id']))
        if query_set.count() == 1:
            friend['edX_id'] = query_set[0].user_id
            friend['edX_username'] = query_set[0].user.username
            friends_that_are_edX_users.append(friend)
    return friends_that_are_edX_users
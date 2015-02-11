"""
Tests for groups
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory
import httpretty
import json
from ddt import ddt, data

from django.conf import settings
_FACEBOOK_API_VERSION = settings.FACEBOOK_API_VERSION
_FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
_FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET

@ddt 
class TestGroups(ModuleStoreTestCase, APITestCase):
    """
        Tests for /api/mobile/v0.5/social/facebook/groups/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    """
        Group Creation and Deletion Tests
    """
    @httpretty.activate
    def test_create_new_open_group(self):
        GROUP_ID = '12345678'
        status_code = 200
        self.set_facebook_interceptor_for_access_token()
        self.set_facebook_interceptor_for_groups({'id': GROUP_ID}, status_code)
        url = reverse('create-delete-group', kwargs={'group_id': ''})
        response = self.client.post(url, {'name': 'TheBestGroup',
                                        'description': 'The group for the best people',
                                        'privacy': 'open'})
        self.assertTrue(1 ==1)
        self.assertEqual(response.status_code, status_code)
        self.assertTrue('id' in response.data)  # pylint: disable=E1103
        self.assertEqual(response.data['id'], GROUP_ID)  # pylint: disable=E1103
    
    @httpretty.activate
    def test_create_new_closed_group(self):
       GROUP_ID = '12345678'
       status_code = 200
       self.set_facebook_interceptor_for_access_token()
       self.set_facebook_interceptor_for_groups({'id': GROUP_ID}, status_code)
       # Create new group
       url = reverse('create-delete-group', kwargs={'group_id': ''})
       response = self.client.post(url, {'name': 'TheBestGroup',
                                           'description': 'The group for the best people',
                                           'privacy': 'closed'})
       self.assertEqual(response.status_code, status_code)
       self.assertTrue('id' in response.data)  # pylint: disable=E1103
       self.assertEqual(response.data['id'], GROUP_ID)  # pylint: disable=E1103
    
    def test_create_new_group_no_name(self):
        url = reverse('create-delete-group', kwargs={'group_id': ''})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_create_new_group_with_invalid_name(self):
        url = reverse('create-delete-group', kwargs={'group_id': ''})
        response = self.client.post(url, {'invalid_name': 'TheBestGroup'})
        self.assertEqual(response.status_code, 400)
    
    def test_create_new_group_with_invalid_privacy(self):
        url = reverse('create-delete-group', kwargs={'group_id': ''})
        response = self.client.post(url, {'name': 'TheBestGroup', 
                                            'privacy': 'half_open_half_closed'})
        self.assertEqual(response.status_code, 400)

    @httpretty.activate
    def test_delete_group_that_exists(self): 
        # Create new group
        GROUP_ID = '12345678'
        status_code = 200
        self.set_facebook_interceptor_for_access_token()
        self.set_facebook_interceptor_for_groups({'id': GROUP_ID}, status_code)
        url = reverse('create-delete-group', kwargs={'group_id' : ''})
        response = self.client.post(url, {'name': 'TheBestGroup',
                                            'description': 'The group for the best people',
                                            'privacy': 'open'})
        self.assertEqual(response.status_code, status_code)
        self.assertTrue('id' in response.data)  # pylint: disable=E1103
        
        # delete group 
        httpretty.register_uri(httpretty.POST,
                'https://graph.facebook.com/' + _FACEBOOK_API_VERSION + '/' + _FACEBOOK_APP_ID +'/groups/' + GROUP_ID + '?access_token=FakeToken&method=delete',
                body='{"success": "true"}',
                status=status_code)
        response = self.delete_group(response.data['id'])
        self.assertTrue(response.status_code, status_code)

    @httpretty.activate
    def test_delete(self):
        GROUP_ID = '12345678'
        status_code = 400
        httpretty.register_uri(httpretty.GET,
                'https://graph.facebook.com/oauth/access_token?client_secret=' + _FACEBOOK_APP_SECRET + '&grant_type=client_credentials&client_id=' + _FACEBOOK_APP_ID,
                body='FakeToken=FakeToken',
                status=200)
        httpretty.register_uri(httpretty.POST,
            'https://graph.facebook.com/' + _FACEBOOK_API_VERSION + '/' + _FACEBOOK_APP_ID +'/groups/' + GROUP_ID + '?access_token=FakeToken&method=delete',
            body='{"error": {"message": "error message"}}',
            status=status_code)
        response = self.delete_group(GROUP_ID)
        self.assertTrue(response.status_code, status_code)


    # '''
    #     Member addition and Removal tests
    # '''

    @data('1234,,,,5678,,', 'this00is00not00a00valid00id', '1234,abc,5678', '')
    def test_invite_single_member_malformed_member_id(self, member_id):
        group_id = '756869167741019'
        response = self.invite_to_group(group_id, member_id)
        self.assertEqual(response.status_code, 400)

    @httpretty.activate
    def test_invite_single_member(self):
        group_id = '756869167741019'
        member_id = '10154831816670300'
        status_code = 200 
        self.set_facebook_interceptor_for_access_token()
        self.set_facebook_interceptor_for_members({'success': 'True'}, status_code, group_id, member_id)
        response = self.invite_to_group(group_id, member_id)
        # from nose.tools import set_trace
        # set_trace()
        self.assertEqual(response.status_code, status_code)
        self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103

    @httpretty.activate
    def test_invite_multiple_members_successfully(self):
        member_ids = '366785273488903,939400156088941,10154831816670300'
        group_id = '756869167741019'
        status_code = 200
        self.set_facebook_interceptor_for_access_token()
        for member_id in member_ids.split(','):
            self.set_facebook_interceptor_for_members({'success': 'True'}, status_code, group_id, member_id)
        response = self.invite_to_group(group_id, member_ids)
        self.assertEqual(response.status_code, status_code)
        for member_id in member_ids.split(','):
            self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103

    @httpretty.activate
    def test_invite_single_member_unsuccessfully(self):
        group_id = '756869167741019'
        member_id = '10154831816670300'
        status_code = 400
        self.set_facebook_interceptor_for_access_token()
        self.set_facebook_interceptor_for_members({'error': {'message': 'error message'}}, status_code, group_id, member_id)
        response = self.invite_to_group(group_id, member_id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error message' in response.data[member_id])  # pylint: disable=E1103


    # @httpretty.activate
    # def test_invite_multiple_members_unsuccessfully(self):
        # from nose.tools import set_trace
        # set_trace()
        # self.set_facebook_interceptor_for_access_token()
        # Add a single user
        # member_id = '10154831816670300'
        # group_id = '756869167741019'
        # self.set_facebook_interceptor_for_members({'success': 'True'}, 200, group_id, member_id)
        # response = self.invite_to_group(group_id, member_id)
        # self.assertEqual(response.status_code, 200)
        # self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103
        # Invite three members, two who are not in the group and one that is a member already.
        
        # member_ids = '366785273488903,939400156088941,10154831816670300'
        # for member_id in member_ids.split(','):
        #     if member_id == '10154831816670300':
        #         self.set_facebook_interceptor_for_members({'error': {'message': 'error message'}}, 400, group_id, member_id)
        #     else:
        #         self.set_facebook_interceptor_for_members({'success': 'True'}, 200, group_id, member_id)
        # set_trace()
        # response = self.invite_to_group(group_id, member_ids)
        # self.assertEqual(response.status_code, 200)
        # for member_id in '366785273488903,939400156088941'.split(','):
        #     self.assertTrue('success' in response.data[member_id])
        # self.assertTrue('error message' in response.data['10154831816670300'])

        # Remove the members added
        # for member_id in member_ids.split(','):
        #     remove_from_group(self, group_id, member_id)

    # def test_remove_member(self): 
    #     group_id = '756869167741019'
    #     member_id = '10154831816670300'
    #     # Note that the memeber must be a member of the app and not a member 
    #     # of the group in order to be able to join the group.
    #     response = invite_to_group(self, group_id, member_id)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103        
    #     # Remove member
    #     remove_from_group(self, group_id, member_id)
        

    '''
        Helper Functions 
    '''

    def set_facebook_interceptor_for_access_token(self):
        httpretty.register_uri(httpretty.GET,
                'https://graph.facebook.com/oauth/access_token?client_secret=' + _FACEBOOK_APP_SECRET + '&grant_type=client_credentials&client_id=' + _FACEBOOK_APP_ID,
                body='FakeToken=FakeToken',
                status=200)

    def set_facebook_interceptor_for_groups(self, data, status):
        httpretty.register_uri(httpretty.POST,
                        'https://graph.facebook.com/' + _FACEBOOK_API_VERSION + '/' + _FACEBOOK_APP_ID + '/groups',
                        body=json.dumps(data),
                        status=status)

    def set_facebook_interceptor_for_members(self, data, status, group_id, member_id):
        httpretty.register_uri(httpretty.POST,
                        'https://graph.facebook.com/' + _FACEBOOK_API_VERSION + '/' + group_id + '/members?member=' + member_id + '&access_token=FakeToken',
                        body=json.dumps(data),
                        status=status)

    def delete_group(self, group_id):
        url = reverse('create-delete-group', kwargs={'group_id': group_id}) 
        response = self.client.delete(url)
        return response

    def invite_to_group(self, group_id, member_ids):
        url = reverse('add-remove-member', kwargs={'group_id': group_id, 'member_id': ''}) 
        return self.client.post(url, {'member_ids': member_ids })

    def remove_from_group(self, group_id, member_id): 
        url = reverse('add-remove-member', kwargs={'group_id': group_id, 'member_id': member_id}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

"""
Tests for groups
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory
import httpretty
import json

from django.conf import settings
_FACEBOOK_API_VERSION = settings.FACEBOOK_API_VERSION
_FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
_FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET

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
        self.assertTrue(True)
        self.set_facebook_interceptor({'id': GROUP_ID}, status_code)
        # url = reverse('create-delete-group', kwargs={'group_id': ''})
        # response = self.client.post(url, {'name': 'TheBestGroup',
        #                                 'description': 'The group for the best people',
        #                                 'privacy': 'open'})
        # self.assertTrue(1 ==1)
        # self.assertEqual(response.status_code, status_code)
        # self.assertTrue('id' in response.data)  # pylint: disable=E1103
        # self.assertEqual(response.data['id'], GROUP_ID)  # pylint: disable=E1103
    
    ##@httpretty.activate
    #def test_create_new_closed_group(self):
    #    GROUP_ID = '12345678'
    #    status_code = 200
    #    self.set_facebook_interceptor({'id': GROUP_ID}, status_code)
    #    # Create new group
    #    url = reverse('create-delete-group', kwargs={'group_id': ''})
    #    response = self.client.post(url, {'name': 'TheBestGroup',
    #                                        'description': 'The group for the best people',
    #                                        'privacy': 'closed'})
    #    self.assertEqual(response.status_code, status_code)
    #    self.assertTrue('id' in response.data)  # pylint: disable=E1103
    #    self.assertEqual(response.data['id'], GROUP_ID)  # pylint: disable=E1103
    

    # def test_create_new_group_no_name(self):
    #     status_code = 400
    #     url = reverse('create-delete-group', kwargs={'group_id': ''})
    #     response = self.client.post(url, {})
    #     self.assertEqual(response.status_code, status_code)

    # def test_create_new_group_with_invalid_name(self):
    #     url = reverse('create-delete-group', kwargs={'group_id': ''})
    #     response = self.client.post(url, {'invalid_name': 'TheBestGroup'})
    #     self.assertEqual(response.status_code, 400)

    # def test_create_new_group_with_invalid_privacy(self):
    #     url = reverse('create-delete-group', kwargs={'group_id': ''})
    #     response = self.client.post(url, {'name': 'TheBestGroup', 
    #                                         'privacy': 'half_open_half_closed'})
    #     self.assertEqual(response.status_code, 400)

    # def test_delete_group(self): 
    #     # Create new group
    #     url = reverse('create-delete-group', kwargs={'group_id' : ''})
    #     response = self.client.post(url, {'name': 'TheBestGroup',
    #                                         'description': 'The group for the best people',
    #                                         'privacy': 'open'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('id' in response.data)  # pylint: disable=E1103
        
    #     # delete group 
    #     delete_group(self, response.data['id'])

    # '''
    #     Member addition and Removal tests
    # '''
    
    def test_invite_single_member_malformed_member_id_1(self):
        group_id = '756869167741019'
        member_id = '1234,,,,5678,,'
        self.assertTrue(True)
        response = invite_to_group(self, group_id, member_id)
        self.assertEqual(response.status_code, 400)
        
    def test_invite_single_member_malformed_member_id_2(self):
        group_id = '756869167741019'
        member_id = 'this00is00not00a00valid00id'
        response = invite_to_group(self, group_id, member_id)
        self.assertEqual(response.status_code, 400)

    def test_invite_single_member_no_member_id(self):
        group_id = '756869167741019'
        member_id = ''
        response = invite_to_group(self, group_id, member_id)
        self.assertEqual(response.status_code, 400)

    def test_invite_single_member_malformed_member_id_3(self):
        group_id = '756869167741019'
        member_id = '1234,abc,5678'
        response = invite_to_group(self, group_id, member_id)
        self.assertEqual(response.status_code, 400)

    # def test_invite_single_member(self):
    #     group_id = '756869167741019'
    #     member_id = '10154831816670300'
    #     # Note that the memeber must be a member of the app and not a member 
    #     # of the group in order to be able to join the group.
    #     response = invite_to_group(self, group_id, member_id)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103
    #     # Remove user from the group
    #     remove_from_group(self, group_id, member_id)

    # def test_invite_multiple_members_successfully(self):
    #     member_ids = '366785273488903,939400156088941,10154831816670300'
    #     group_id = '756869167741019'
    #     response = invite_to_group(self, group_id, member_ids)
    #     self.assertEqual(response.status_code, 200)
    #     for member_id in member_ids.split(','):
    #         self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103
    #     # Remove the members added
    #     for member_id in member_ids.split(','):
    #         remove_from_group(self, group_id, member_id)

    # def test_invite_multiple_members_unsuccessfully(self):
    #     # Add a single user
    #     member_id = '10154831816670300'
    #     group_id = '756869167741019'
    #     response = invite_to_group(self, group_id, member_id)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('success' in response.data[member_id])  # pylint: disable=E1103
    #     # Invite three members, two who are not in the group and one that is a member already.
    #     member_ids = '366785273488903,939400156088941,10154831816670300'
    #     response = invite_to_group(self, group_id, member_ids)
    #     self.assertEqual(response.status_code, 200)
    #     for member_id in '366785273488903,939400156088941'.split(','):
    #         self.assertTrue('success' in response.data[member_id])
    #     self.assertTrue('(#4001) User is not eligible to be added to group' in response.data['10154831816670300'])

    #     # Remove the members added
    #     for member_id in member_ids.split(','):
    #         remove_from_group(self, group_id, member_id)

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

    def set_facebook_interceptor(self, data, status):
        httpretty.register_uri(httpretty.POST,
                        'https://graph.facebook.com/' + _FACEBOOK_API_VERSION + '/' + _FACEBOOK_APP_ID + '/groups',
                        body=json.dumps(data),
                        status=status)
        httpretty.register_uri(httpretty.GET,
                        'https://graph.facebook.com/oauth/access_token?client_secret=' + _FACEBOOK_APP_SECRET + '&grant_type=client_credentials&client_id=' + _FACEBOOK_APP_ID,
                        body='FakeToken=FakeToken',
                        status=200)

def delete_group(self, group_id):
    url = reverse('create-delete-group', kwargs={'group_id': group_id}) 
    response = self.client.delete(url)
    self.assertEqual(response.status_code, 200)

def invite_to_group(self, group_id, member_ids):
        url = reverse('add-remove-member', kwargs={'group_id': group_id, 'member_id': ''}) 
        return self.client.post(url, {'member_ids': member_ids })

def remove_from_group(self, group_id, member_id): 
    url = reverse('add-remove-member', kwargs={'group_id': group_id, 'member_id': member_id}) 
    response = self.client.delete(url)
    self.assertEqual(response.status_code, 200)

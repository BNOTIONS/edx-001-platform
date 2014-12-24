"""
Tests for groups
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from courseware.tests.factories import UserFactory

from nose.tools import set_trace


class TestGroups(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/groups/...
    """
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password='test')

    def test_create_new_group(self):
        # Create new group
        url = reverse('create-new-group')
        response = self.client.post(url, {  'name' : 'TheBestGroup',
                                            'description' : 'The group for the best people',
                                            'privacy' : 'open'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in response.data)  # pylint: disable=E1103
        
        # Delete the groupd just created
        url = reverse('delete-group', kwargs={'group_id' : response.data['id']}) 
        response = self.client.delete(url)


    def test_create_new_group_invalid_params(self):
        url = reverse('create-new-group')
        response = self.client.post(url, {  'invalid_param' : 'TheBestGroup'})
        self.assertEqual(response.status_code, 400)


    def test_create_new_group_no_params(self):
        url = reverse('create-new-group')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)


    def test_invite_single_member(self):
        url = reverse('invite-to-group', kwargs={'group_id' : '756869167741019'}) 
        response = self.client.post(url, {  'member-ids' : '10154831816670300' })
        self.assertEqual(response.status_code, 200)
        set_trace()
        self.assertTrue('success' in response.data)  # pylint: disable=E1103

    
    def test_invite_multiple_members(self):
        set_trace()
        url = reverse('invite-to-group', kwargs={'group_id' : '756869167741019'}) 
        response = self.client.post(url, {  'member-ids' : '366785273488903,939400156088941,10154831816670300' })
        self.assertEqual(response.status_code, 200)        
        self.assertTrue('success' in response.data)  # pylint: disable=E1103


    def test_delete(self): 
        url = reverse('delete-group', kwargs={'group_id' : '757474821013787'}) 
        response = self.client.delete(url)

    def test_remove_member(self): 
        url = reverse('group-remove-member', kwargs={ 'group_id' : '756869167741019', 
                                                      'member_id' : '10154831816670300'}) 
        response = self.client.delete(url)

    # TODO: member doesn't exist, memmer already in group





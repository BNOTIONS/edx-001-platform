"""
Serializer for user API
"""
from rest_framework import serializers
from rest_framework.reverse import reverse


class CoursesWithFriendsSerializer(serializers.Serializer):
	"""
		Serializes facebook groups request
	"""
	oauth_token = serializers.CharField(required=True)

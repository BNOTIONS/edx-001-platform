"""
Serializer for Share Settings API
"""
from rest_framework import serializers

from nose.tools import set_trace

class UserSharingSerializar(serializers.Serializer):
	"""
	Serializes user social settings
	"""
	share_pref = serializers.BooleanField(default=True, required=True)

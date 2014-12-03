"""
Serializer for Share Settings API
"""
from rest_framework import serializers


class UserSharingSerializar(serializers.Serializer):
	"""
	Serializes user social settings
	"""
	share_pref = serializers.BooleanField(default=True, required=True)

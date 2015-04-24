# REST_FRAMEWORK
from rest_framework import serializers

# homepage module
from .models import *

# meSerialized = serializers.DeviceSerializer(self).data
# cache.set('device:{0}'.format(self.id), json.dumps(meSerialized))


class DeviceRedisSerializer(serializers.Serializer):
    pass


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer class for the device model"""

    class Meta:
        model = Device

    def validate(self, data):
        """Check that atleast one significant field is passed."""

        if all(v is None for v in
                (data['magnification'],
                 data['field_of_view'],
                 data['view_range'])):
            raise serializers.ValidationError(
                "Cannot save model if all significant fields"
                " (other than device_name) are absent.")
        return data

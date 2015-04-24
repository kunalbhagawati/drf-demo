import json

from django.core.exceptions import ValidationError
from django.db import models


class Device(models.Model):
    """Model for the zooming devices"""

    device_name = models.CharField(db_index=True, max_length=50)
    magnification = models.DecimalField(
            db_index=True,
            null=True,
            max_digits=5,
            decimal_places=2)
    field_of_view = models.DecimalField(
            db_index=True,
            null=True,
            max_digits=5,
            decimal_places=2)
    view_range = models.DecimalField(
            db_index=True,
            null=True,
            max_digits=7,
            decimal_places=2)

    def save(self, *args, **kwargs):
        if all(v is None for v in
                (self.magnification, self.field_of_view, self.view_range)):
            raise ValidationError("Cannot save model if all significant fields"
                " (other than device_name) are absent.")
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}: {1}".format(self.id, self.device_name)

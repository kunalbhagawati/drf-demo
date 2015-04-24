# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20150419_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='device',
            name='field_of_view',
            field=models.DecimalField(db_index=True, max_digits=5, null=True, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='device',
            name='magnification',
            field=models.DecimalField(db_index=True, max_digits=5, null=True, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='device',
            name='view_range',
            field=models.DecimalField(db_index=True, max_digits=7, null=True, decimal_places=2),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='field_of_view',
            field=models.DecimalField(max_digits=5, null=True, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='device',
            name='magnification',
            field=models.DecimalField(max_digits=5, null=True, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='device',
            name='view_range',
            field=models.DecimalField(max_digits=7, null=True, decimal_places=2),
        ),
    ]

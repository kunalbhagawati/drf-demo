# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('device_name', models.CharField(max_length=50)),
                ('magnification', models.DecimalField(max_digits=3, decimal_places=2)),
                ('field_of_view', models.DecimalField(max_digits=3, decimal_places=2)),
                ('view_range', models.DecimalField(max_digits=3, decimal_places=2)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-03 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speak', '0005_auto_20170203_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='Audio_Urdu',
            field=models.TextField(max_length=2000),
        ),
    ]

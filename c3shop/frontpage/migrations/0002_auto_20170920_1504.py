# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-20 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='changeReason',
            field=models.CharField(max_length=15000, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamwork', 'load_data1'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='teamwork.Project'),
            preserve_default=False,
        ),
    ]

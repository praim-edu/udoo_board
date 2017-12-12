# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoundTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts_at', models.DateTimeField(verbose_name='starts at')),
                ('ends_at', models.DateTimeField(verbose_name='ends at')),
                ('file_name', models.CharField(max_length=250)),
                ('max_volume', models.IntegerField(verbose_name='max volume level')),
                ('min_volume', models.IntegerField(verbose_name='min volume level')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-23 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0007_auto_20180322_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('log_from', models.CharField(max_length=128)),
                ('log_message', models.TextField(blank=True)),
            ],
        ),
    ]
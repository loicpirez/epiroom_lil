# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-22 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0004_auto_20180322_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='description',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Api.User'),
        ),
    ]

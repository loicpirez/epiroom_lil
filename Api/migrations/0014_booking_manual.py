# Generated by Django 2.0 on 2018-11-13 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0013_room_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='manual',
            field=models.BooleanField(default=False),
        ),
    ]

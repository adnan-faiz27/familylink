# Generated by Django 4.2 on 2023-09-09 15:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0011_alter_member_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='photo2',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='member',
            name='photo3',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images/'),
        ),
        migrations.RemoveField(
            model_name='member',
            name='father',
        ),
        migrations.AddField(
            model_name='member',
            name='father',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

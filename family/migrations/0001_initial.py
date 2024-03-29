# Generated by Django 4.2 on 2023-09-08 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('familyID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=35)),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('firstName', models.CharField(max_length=20)),
                ('middleName', models.CharField(blank=True, max_length=20)),
                ('lastName', models.CharField(blank=True, max_length=20)),
                ('mobileNo', models.IntegerField(blank=True)),
                ('address1', models.TextField(blank=True, max_length=50, verbose_name='Address line 1')),
                ('country', models.CharField(blank=True, max_length=15, verbose_name='Country')),
                ('city', models.CharField(blank=True, max_length=15, verbose_name='City')),
                ('photo1', models.ImageField(blank=True, default='', null=True, upload_to='images/')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('FID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='family.family')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('mother', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]

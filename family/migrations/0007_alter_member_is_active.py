# Generated by Django 4.2 on 2023-09-09 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0006_alter_member_father_alter_member_mother'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

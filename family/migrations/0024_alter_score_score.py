# Generated by Django 4.2 on 2023-10-14 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0023_room_remove_member_photo1_remove_member_photo2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
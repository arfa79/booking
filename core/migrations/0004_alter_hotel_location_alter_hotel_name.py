# Generated by Django 5.1 on 2024-12-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_hotel_location_alter_hotel_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='location',
            field=models.CharField(max_length=200, verbose_name='Hotel Location'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Hotel Name'),
        ),
    ]

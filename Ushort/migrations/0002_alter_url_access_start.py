# Generated by Django 4.0.1 on 2022-03-09 14:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Ushort', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='access_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

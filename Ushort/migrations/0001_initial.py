# Generated by Django 4.0.1 on 2022-02-21 19:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='-', max_length=50, unique=True)),
                ('code', models.CharField(default='-', help_text='ISO 3166-1 alpha-2 codes are two-letter country codes', max_length=2, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('account_type', models.TextField(choices=[('F', 'Free'), ('A', 'Advanced'), ('C', 'Complete')], default='F', max_length=1)),
                ('max_url', models.IntegerField(default=25, help_text='Maximum number of URLs a creator can generate')),
                ('max_url_a_day', models.IntegerField(default=5, help_text='Maximum number of URLs a creator can generate per day')),
                ('max_monitored_url', models.IntegerField(default=0, help_text='Maximum number of Monitored-URLs a creator can generate')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=10, unique=True)),
                ('target', models.URLField()),
                ('visitors', models.IntegerField(default=0)),
                ('visitors_after_expire', models.IntegerField(default=0)),
                ('access_start', models.DateTimeField(auto_now_add=True)),
                ('access_duration', models.DurationField(default=datetime.timedelta(days=10), help_text='Duration of access to the URL')),
                ('access_code', models.CharField(blank=True, default='', help_text='Restricts access to this URL with the access code', max_length=64, null=True)),
                ('monitored', models.BooleanField(default=False, help_text='If checked, time, date, country and number of visitors will be collected for the URL until it expires')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Ushort.creator', to_field='email')),
            ],
            options={
                'ordering': ['creator', '-created'],
                'get_latest_by': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('hour', models.IntegerField(choices=[(0, '00:00 - 01:59'), (2, '02:00 - 03:59'), (4, '04:00 - 05:59'), (6, '06:00 - 07:59'), (8, '08:00 - 09:59'), (10, '10:00 - 11:59'), (12, '12:00 - 13:59'), (14, '14:00 - 15:59'), (16, '16:00 - 17:59'), (18, '18:00 - 19:59'), (20, '20:00 - 21:59'), (22, '22:00 - 23:59')], help_text='Stores the visit time in 2-hour timeframes')),
                ('number', models.IntegerField(default=0)),
                ('country', models.ForeignKey(default='-', on_delete=django.db.models.deletion.DO_NOTHING, to='Ushort.country', to_field='name')),
                ('url', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ushort.url')),
            ],
            options={
                'ordering': ['-date', 'url', '-number'],
                'get_latest_by': 'date',
            },
        ),
    ]

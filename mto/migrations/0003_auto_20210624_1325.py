# Generated by Django 3.2.4 on 2021-06-24 07:55

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mto', '0002_mto_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mto',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='mto',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='mto',
            name='contact_number',
            field=models.IntegerField(default=1234),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mto',
            name='job_category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mto',
            name='location',
            field=models.CharField(default='India', max_length=20),
            preserve_default=False,
        ),
    ]
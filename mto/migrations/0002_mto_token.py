# Generated by Django 3.2 on 2021-06-21 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mto',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

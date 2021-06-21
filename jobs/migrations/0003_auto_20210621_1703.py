# Generated by Django 3.2 on 2021-06-21 11:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_microtask_quantity_job'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='malrequirement',
            options={'verbose_name': 'Mal Requirement', 'verbose_name_plural': 'Mal Requirements'},
        ),
        migrations.AddField(
            model_name='malrequirement',
            name='micro_task_category',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='malrequirement',
            name='person_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='malrequirement',
            name='identification_number',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='malrequirement',
            name='job_instructions',
            field=models.FileField(upload_to='job_documents/instruction'),
        ),
        migrations.AlterField(
            model_name='malrequirement',
            name='job_sample',
            field=models.FileField(upload_to='job_documents/sample'),
        ),
        migrations.AlterField(
            model_name='malrequirement',
            name='micro_task',
            field=models.CharField(max_length=300),
        ),
    ]
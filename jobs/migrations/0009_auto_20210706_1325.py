# Generated by Django 3.2.4 on 2021-07-06 07:55

from django.db import migrations, models
import jobs.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_jobs_job_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='job_instructions',
        ),
        migrations.RemoveField(
            model_name='jobs',
            name='job_sample',
        ),
        migrations.RemoveField(
            model_name='microtask',
            name='job_instructions',
        ),
        migrations.RemoveField(
            model_name='microtask',
            name='job_sample',
        ),
        migrations.AddField(
            model_name='microtask',
            name='instructions',
            field=models.FileField(
                default='Onkar_py.txt', upload_to=jobs.models.instructions_directory_path),
        ),
        migrations.AddField(
            model_name='microtask',
            name='sample',
            field=models.FileField(
                default='Onkar_py.txt', upload_to=jobs.models.sample_directory_path),
        ),
        migrations.AddField(
            model_name='mtojob',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_status',
            field=models.CharField(choices=[('cr', 'Created'), ('as', 'Assigned'), (
                'ur', 'Under review'), ('co', 'Completed')], default='cr', max_length=100),
        ),
        migrations.AlterField(
            model_name='mtojob',
            name='job_status',
            field=models.CharField(choices=[('in', 'in progress'), (
                'sub', 'submitted'), ('co', 'Completed')], default='in', max_length=100),
        ),
        migrations.AlterField(
            model_name='mtojob',
            name='payment_status',
            field=models.CharField(choices=[('uninitiated', 'uninitiated'), (
                'pending', 'pending'), ('paid', 'paid')], default='uninitiated', max_length=100),
        ),
    ]

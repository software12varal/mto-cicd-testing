# Generated by Django 3.2.4 on 2021-06-28 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_merge_20210628_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtojob',
            name='job_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.jobstatus', verbose_name='job_status_name'),
        ),
        migrations.AlterField(
            model_name='jobstatus',
            name='job_status_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='paymentstatus',
            name='payment_status',
            field=models.CharField(max_length=200),
        ),
    ]
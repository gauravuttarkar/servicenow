# Generated by Django 2.0.6 on 2018-06-12 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0015_servicenow_model_instance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userintegration',
            name='webhook_id',
        ),
        migrations.AddField(
            model_name='servicenow_model',
            name='webhook_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
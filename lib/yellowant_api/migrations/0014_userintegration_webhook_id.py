# Generated by Django 2.0.6 on 2018-06-12 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0013_auto_20180608_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='userintegration',
            name='webhook_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]

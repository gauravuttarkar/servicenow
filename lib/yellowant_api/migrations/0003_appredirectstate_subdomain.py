# Generated by Django 2.0.6 on 2018-06-18 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0002_yellowantredirectstate_subdomain'),
    ]

    operations = [
        migrations.AddField(
            model_name='appredirectstate',
            name='subdomain',
            field=models.CharField(default='devacc', max_length=128),
            preserve_default=False,
        ),
    ]

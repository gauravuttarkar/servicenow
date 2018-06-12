# Generated by Django 2.2.dev20180521165340 on 2018-05-28 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0002_yellowantredirectstate'),
    ]

    operations = [
        migrations.CreateModel(
            name='azure',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='yellowant_api.UserIntegration')),
                ('AZURE_tenant_id', models.CharField(max_length=200)),
                ('AZURE_client_id', models.CharField(max_length=200)),
                ('AZURE_subscription_id', models.CharField(max_length=200)),
            ],
        ),
    ]

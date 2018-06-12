# Generated by Django 2.0.6 on 2018-06-04 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0007_auto_20180604_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicenow_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=200)),
                ('update_login_flag', models.BooleanField(default=False, max_length=2)),
                ('user_integration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yellowant_api.UserIntegration')),
            ],
        ),
    ]

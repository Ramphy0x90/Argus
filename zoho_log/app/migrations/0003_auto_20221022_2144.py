# Generated by Django 2.2.12 on 2022-10-22 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_department_zoho_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='log_out',
            field=models.DateTimeField(null=True),
        ),
    ]
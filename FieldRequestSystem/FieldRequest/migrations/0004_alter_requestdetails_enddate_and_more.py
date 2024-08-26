# Generated by Django 5.0.2 on 2024-08-24 06:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FieldRequest', '0003_alter_requestdetails_s_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestdetails',
            name='endDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='requestdetails',
            name='startDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

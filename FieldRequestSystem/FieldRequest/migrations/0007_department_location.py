# Generated by Django 5.0.2 on 2024-09-09 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FieldRequest', '0006_requestdetails_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='location',
            field=models.CharField(default='Dar es Salaam', max_length=100),
        ),
    ]

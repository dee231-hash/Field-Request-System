# Generated by Django 5.0.2 on 2024-09-06 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FieldRequest', '0005_department_alter_requestdetails_enddate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestdetails',
            name='region',
            field=models.CharField(default='Dar es Salaam', max_length=100),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-23 16:18

import students.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='roll',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[students.models.validate_numeric]),
        ),
    ]

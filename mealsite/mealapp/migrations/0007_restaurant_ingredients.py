# Generated by Django 2.1.7 on 2019-03-25 13:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealapp', '0006_auto_20190325_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='ingredients',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), default=list, size=None),
        ),
    ]
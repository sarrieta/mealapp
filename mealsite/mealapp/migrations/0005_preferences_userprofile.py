# Generated by Django 2.1.5 on 2019-01-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealapp', '0004_auto_20190115_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferences', models.CharField(max_length=4096)),
            ],
            options={
                'verbose_name': 'preference',
                'verbose_name_plural': 'preferences',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=15)),
                ('password', models.CharField(default=None, max_length=15)),
                ('preferences', models.ManyToManyField(blank=True, related_name='related_to', to='mealapp.Preferences')),
            ],
        ),
    ]

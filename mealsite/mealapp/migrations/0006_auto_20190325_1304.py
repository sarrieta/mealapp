# Generated by Django 2.1.7 on 2019-03-25 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('mealapp', '0005_menu_items_cuisine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='preferences',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_ptr',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='neighbourhood',
        ),
        migrations.DeleteModel(
            name='Preferences',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

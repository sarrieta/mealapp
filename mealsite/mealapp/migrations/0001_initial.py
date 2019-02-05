# Generated by Django 2.0.10 on 2019-01-31 14:51

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=30)),
                ('item_name', models.CharField(default=None, max_length=30)),
                ('item_description', models.CharField(default=None, max_length=500)),
                ('item_price', models.FloatField(default=None, max_length=2)),
            ],
            options={
                'verbose_name': 'Menu Item',
                'verbose_name_plural': 'Menu Items',
            },
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferences', models.CharField(default=None, max_length=15)),
            ],
            options={
                'verbose_name_plural': 'preferences',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=30)),
                ('opening', models.CharField(default=None, max_length=150)),
                ('long', models.DecimalField(decimal_places=9, max_digits=15, null=True)),
                ('lat', models.DecimalField(decimal_places=9, max_digits=15, null=True)),
                ('description', models.TextField(default=None, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=60, null=True)),
            ],
            options={
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('preferences', models.ManyToManyField(blank=True, related_name='related_to', to='mealapp.Preferences')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='menu_items',
            name='restaurant_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealapp.Restaurant'),
        ),
    ]

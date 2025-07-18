# Generated by Django 5.1.6 on 2025-05-21 19:00

import django.utils.timezone
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', users.models.CustomUserIDField(editable=False, max_length=6, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('business', 'Business Owner'), ('superadmin', 'Super Admin')], default='customer', max_length=20)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('device_token', models.CharField(blank=True, max_length=255, null=True)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_mute', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]

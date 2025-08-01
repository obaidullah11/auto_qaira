# Generated by Django 5.1.6 on 2025-05-26 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('year', models.PositiveIntegerField()),
                ('transmission', models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=10)),
                ('fuel_type', models.CharField(choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Hybrid', 'Hybrid'), ('Electric', 'Electric')], max_length=10)),
                ('engine_capacity', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=30)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('mileage', models.PositiveIntegerField()),
                ('seating_capacity', models.PositiveSmallIntegerField()),
                ('car_type', models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'), ('Convertible', 'Convertible'), ('Truck', 'Truck'), ('Van', 'Van')], max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('pickup_location', models.CharField(max_length=255)),
                ('available_from', models.DateField()),
                ('available_until', models.DateField()),
                ('availability_type', models.CharField(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], max_length=10)),
                ('delivery_available', models.BooleanField(default=False)),
                ('price_per_day', models.PositiveIntegerField()),
                ('price_per_week', models.PositiveIntegerField()),
                ('price_per_month', models.PositiveIntegerField()),
                ('security_deposit', models.PositiveIntegerField()),
                ('minimum_rent_days', models.PositiveIntegerField()),
                ('registration_card', models.ImageField(upload_to='documents/')),
                ('insurance_document', models.FileField(upload_to='documents/')),
                ('owner_cnic', models.ImageField(upload_to='documents/')),
                ('air_conditioning', models.BooleanField(default=True)),
                ('gps', models.BooleanField(default=False)),
                ('bluetooth', models.BooleanField(default=False)),
                ('usb_charging', models.BooleanField(default=False)),
                ('child_seat', models.BooleanField(default=False)),
                ('fuel_policy', models.CharField(choices=[('Full to Full', 'Full to Full'), ('Prepaid', 'Prepaid')], max_length=20)),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('driver_allowed', models.BooleanField(default=True)),
                ('with_driver_only', models.BooleanField(default=False)),
                ('driver_charges_per_day', models.PositiveIntegerField(default=0)),
                ('max_km_per_day', models.PositiveIntegerField()),
                ('extra_km_charge', models.PositiveIntegerField()),
                ('cancellation_policy', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='car_images/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_images', to='car_onboarding.carlisting')),
            ],
        ),
    ]

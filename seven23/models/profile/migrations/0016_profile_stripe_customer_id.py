# Generated by Django 4.2.7 on 2023-12-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0015_remove_profile_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

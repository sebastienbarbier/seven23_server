# Generated by Django 4.2.7 on 2023-11-27 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0008_remove_charge_coupon_alter_charge_paiment_method_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Charge',
        ),
    ]

# Generated by Django 2.1.8 on 2019-07-06 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_currency_code'),
        ('accounts', '0004_auto_20170224_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='currencies',
            field=models.ManyToManyField(to='currency.Currency'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-25 03:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termsandconditions',
            name='markdown',
            field=models.TextField(help_text='Formatted in Markdown', verbose_name='Terms and conditions'),
        ),
    ]
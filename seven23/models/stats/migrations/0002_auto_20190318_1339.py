# Generated by Django 2.1 on 2019-03-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyactiveuser',
            options={'ordering': ('year', 'month', 'day')},
        ),
        migrations.AlterModelOptions(
            name='monthlyactiveuser',
            options={'ordering': ('year', 'month')},
        ),
        migrations.AlterField(
            model_name='dailyactiveuser',
            name='day',
            field=models.IntegerField(default=18, editable=False, verbose_name='Day'),
        ),
    ]
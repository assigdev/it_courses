# Generated by Django 2.0.4 on 2018-04-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_auto_20180423_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinlesson',
            name='attendance',
            field=models.BooleanField(default=False, verbose_name='Был на занятии'),
        ),
    ]

# Generated by Django 2.0.4 on 2018-04-18 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='have_time',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='time',
        ),
    ]

# Generated by Django 2.0.4 on 2018-04-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20180418_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinlesson',
            name='attendance',
            field=models.NullBooleanField(default=False, verbose_name='Был на занятии'),
        ),
        migrations.AlterField(
            model_name='studentinlesson',
            name='quiz_status',
            field=models.CharField(choices=[('on_first', 'Пройден с первого раза'), ('on_second', 'Пройден со второго раза'), ('on_third', 'Пройден со третьего раза'), ('off_first', 'Не пройден с первого раза'), ('off_second', 'Не пройден со второго раза'), ('off', 'Провален'), ('not_start', 'Не начат')], default='not_start', max_length=9, verbose_name='Статус тестирования'),
        ),
    ]

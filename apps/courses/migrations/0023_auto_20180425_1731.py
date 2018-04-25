# Generated by Django 2.0.4 on 2018-04-25 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_auto_20180423_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinlesson',
            name='is_homework_final',
            field=models.BooleanField(default=False, verbose_name='ДЗ сдана'),
        ),
        migrations.AlterField(
            model_name='studentinlesson',
            name='is_homework_in_deadline',
            field=models.NullBooleanField(default=None, verbose_name='ДЗ сдано в срок'),
        ),
        migrations.AlterField(
            model_name='studentinlesson',
            name='is_quiz_in_deadline',
            field=models.NullBooleanField(default=None, verbose_name='Тест сдан в срок'),
        ),
        migrations.AlterField(
            model_name='studentinlesson',
            name='quiz_status',
            field=models.CharField(choices=[('on', 'Пройден'), ('off', 'Провален'), ('not_start', 'Не начат')], default='not_start', max_length=9, verbose_name='Статус тестирования'),
        ),
    ]
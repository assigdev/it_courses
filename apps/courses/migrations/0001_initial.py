# Generated by Django 2.0.4 on 2018-04-16 10:18

import apps.courses.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from ckeditor_uploader.fields import RichTextUploadingField
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizzes', '0001_initial'),
        ('course_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('img', stdimage.models.StdImageField(blank=True, upload_to=apps.courses.models.get_img_path, verbose_name='Фотография')),
                ('slug', models.SlugField(max_length=20)),
                ('state', models.CharField(choices=[('active', 'Активен'), ('close', 'Завершен'), ('reg', 'Набор, регистрация')], max_length=6, verbose_name='статус')),
                ('max_user_count', models.PositiveSmallIntegerField(verbose_name='Максимальное количество учащихся')),
                ('preview', models.TextField(max_length=300, verbose_name='Превью описание')),
                ('about', RichTextUploadingField(verbose_name='Описание курса')),
                ('start_date', models.DateField(verbose_name='Дата начала курса')),
                ('end_date', models.DateField(verbose_name='Дата завершения курса')),
                ('selection_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quizzes.Quiz', verbose_name='Отборочный тест')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_test', 'На тестирование'), ('in_view', 'На собеседовании'), ('active', 'Проходит курс'), ('fail', 'Исключен из курса'), ('fail_test', 'Не прошел собеседование'), ('fail_view', 'Не прошел тестирование'), ('finish', 'Окончил курс')], max_length=9, verbose_name='Статус')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_users.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=20)),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='Номер занятия')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата занятия')),
                ('content', RichTextUploadingField(blank=True, verbose_name='Материал занятия')),
                ('home_work', RichTextUploadingField(blank=True, verbose_name='Домашнее задание')),
                ('home_work_deadline', models.DateField(blank=True, verbose_name='Дедлайн для домашней работы')),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quizzes.Quiz', verbose_name='Тестирование')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentInLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.BooleanField(default=True, verbose_name='Был на занятии')),
                ('is_homework_final', models.BooleanField(default=False, verbose_name='Сдана')),
                ('is_homework_in_deadline', models.NullBooleanField(default=None, verbose_name='В срок')),
                ('quiz_status', models.CharField(choices=[('on_first', 'Пройден с первого раза'), ('on_second', 'Пройден со второго раза'), ('on_third', 'Пройден со третьего раза'), ('off_first', 'Не пройден с первого раза'), ('off_second', 'Не пройден со второго раза'), ('off', 'Провален'), ('not_start', 'Не начат')], max_length=9, verbose_name='Статус тестирования')),
                ('is_quiz_in_deadline', models.NullBooleanField(default=None, verbose_name='В срок')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson', verbose_name='Занятие')),
                ('quiz_result', models.ForeignKey(on_delete='Результат тестирования', to='quizzes.QuizResult')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_users.Student', verbose_name='ученик')),
            ],
            options={
                'verbose_name': 'Студент на занятии',
                'verbose_name_plural': 'Студенты на занятиях',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(through='courses.CourseStudent', to='course_users.Student', verbose_name='Студенты'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(to='course_users.Teacher', verbose_name='Учителя'),
        ),
    ]

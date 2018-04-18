from django.db import models
from martor.models import MartorField


class Quiz(models.Model):
    title = models.CharField('Название теста', max_length=200)
    slug = models.SlugField('Ссылка на сайте', max_length=200)
    result = models.PositiveSmallIntegerField('Процент правильных ответов',
                                              default=0,
                                              help_text='Процент, по которому проверяется, прошел ли тест пользователь')
    open = models.BooleanField(
        'Открыть подробные результаты',
        default=False,
        help_text="Если включить, то после прохождения теста, пользователь увидит, где и как он ошибся"
    )

    class Meta:
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'

    def __str__(self):
        return self.title


QUESTION_TYPE = (
    ('chr', 'Один ответ'),
    ('var', 'Один верный из вариантов'),
)


class Question(models.Model):
    content = MartorField('текст вопроса', blank=True)
    quiz = models.ForeignKey(Quiz, verbose_name='Тестирования', on_delete=models.CASCADE, related_name='questions')
    type = models.CharField('Тип вопроса', choices=QUESTION_TYPE, max_length=3, default='var')
    chr_answer = models.CharField('Верный ответ', max_length=100, blank=True)
    position = models.SmallIntegerField('Позиция', default=0)

    class Meta:
        verbose_name = 'Вопрос для Тестирования'
        verbose_name_plural = 'Вопросы для Тестирования'

    def __str__(self):
        return self.content


class AnswerVar(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    content = MartorField('текст ответа', blank=True)
    is_true = models.BooleanField('Верный ответ', default=False)
    position = models.SmallIntegerField('Позиция', default=0)

    class Meta:
        verbose_name = 'Ответ: один верный'
        verbose_name_plural = 'Ответы: один верный'

    def __str__(self):
        return self.content


class QuizResult(models.Model):
    # student_in_lesson = models.ForeignKey(StudentInLesson, verbose_name='пользователь', on_delete=models.CASCADE, related_name='answers')
    quiz = models.ForeignKey(Quiz,
                             verbose_name='Тестирование',
                             related_name='users_answers',
                             on_delete=models.CASCADE)
    result = models.PositiveSmallIntegerField('Процент правильных ответов', default=0)

    class Meta:
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'


class StudentAnswer(models.Model):
    user_answer = models.ForeignKey(QuizResult, verbose_name='Тест с ответами пользователя',  on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    answer_var = models.ForeignKey(AnswerVar, verbose_name='Ответ: один верный', on_delete=models.CASCADE)
    answer_chr = models.CharField('Текстовый ответ', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Ответ студента'
        verbose_name_plural = 'Ответы студентов'

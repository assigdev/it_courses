from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


TEMPLATES = (
    ('default.html', 'По умолчанию'),
    ('home.html', 'Главная'),
)


class Page(models.Model):
    title = models.CharField("Название страницы", max_length=100)
    slug = models.SlugField("url", max_length=100)
    sort = models.SmallIntegerField("Позиция", default=1)
    template = models.CharField("Шаблон", max_length=100, choices=TEMPLATES)
    content = RichTextUploadingField("Контент", max_length=10000, blank=True)
    meta_keywords = models.CharField("Ключевые слова", max_length=100, blank=True)
    meta_description = models.TextField("Meta описание(description)", max_length=400, blank=True)
    meta_tags = models.TextField("Другие Meta теги", max_length=400, blank=True)
    scripts = models.TextField("Скрипты", max_length=500, blank=True)

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['sort', 'id']

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'page:page', (self.slug,)

    def get_template(self):
        return 'main/%s' % self.template

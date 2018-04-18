from slugify import Slugify


class ModelAutoSlugMixin(object):
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = self._generate_slug(self.id, self.title)
        super(ModelAutoSlugMixin, self).save()

    @staticmethod
    def _generate_slug(lesson_id, title):
        custom_slugify = Slugify(to_lower=True)
        return "{0}_{1}".format(lesson_id, format(custom_slugify(title[:12])))

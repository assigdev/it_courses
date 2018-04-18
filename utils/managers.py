from django.db import models
from django.utils import timezone


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(active=True)


class ActiveDateManager(models.Manager):
    def get_queryset(self):
        return super(ActiveDateManager, self).get_queryset().filter(active=True) \
            .filter(created_at__lt=timezone.localtime(timezone.now()))

from stdimage.utils import pre_delete_delete_callback, pre_save_delete_callback
from django.db.models.signals import post_delete, pre_save


def img_files_del(*clses):
    for cls in clses:
        post_delete.connect(pre_delete_delete_callback, sender=cls)
        pre_save.connect(pre_save_delete_callback, sender=cls)

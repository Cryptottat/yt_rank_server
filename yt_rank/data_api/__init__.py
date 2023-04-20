from django.contrib.contenttypes.models import ContentType
from django.utils.functional import Promise
from django.db.models.signals import post_migrate


def update_contenttypes_names(**kwargs):
    for c in ContentType.objects.all():
        cl = c.model_class()
        # Promises classes are from translated, mostly django-internal models. ignore them.
        if cl and not isinstance(cl._meta.verbose_name, Promise):
            new_name = cl._meta.verbose_name.decode('utf-8')
            if c.name != new_name:
                c.name = new_name
                c.save()


post_migrate.connect(update_contenttypes_names, dispatch_uid="update_contenttypes")

from django.db import models


class TimeStampedModel(models.Model):

    """ Core Model """

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        abstract = True

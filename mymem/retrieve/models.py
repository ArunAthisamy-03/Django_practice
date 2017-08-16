from __future__ import unicode_literals
from django.db import models


class Questions(models.Model):
    question = models.TextField()

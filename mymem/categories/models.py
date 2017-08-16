from __future__ import unicode_literals
from django.db import models


class Answers(models.Model):
    question = models.TextField()
    answer = models.TextField()
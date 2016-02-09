from django.db import models
import sys, os


class created_documents(models.Model):
    gene = models.TextField()
    transcript = models.CharField(max_length=40)
    location = models.TextField()
    created_on = models.DateTimeField()

from django.db import models

# Create your models here.

class created_documents(models.Model):
    transcript = models.CharField(max_length=40)
    location = models.TextField()
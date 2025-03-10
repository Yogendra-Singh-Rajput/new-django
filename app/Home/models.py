from django.db import models

# Create your models here.

class contact_form(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    category = models.TextField()
    description = models.TextField()
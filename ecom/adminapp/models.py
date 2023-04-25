from django.db import models

# Create your models here.
class Banner(models.Model):
    image = models.ImageField(upload_to='user', null=True, blank=True)
    updated_at = models.DateField(auto_now=True)
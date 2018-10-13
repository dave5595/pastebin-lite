from django.db import models

# Create your models here.
class Paste (models.Model):
    char_id = models.CharField(max_length=8, db_index=True)
    title = models.CharField(max_length=128)
    expiration_datetime = models.DateTimeField(null=True, blank=True)
    # Is the paste removed (removed from view but not deleted)
    removed = models.IntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True, db_index=True)


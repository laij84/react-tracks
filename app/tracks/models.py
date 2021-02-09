from django.db import models


class Track(models.Model):
    # id field automatically added, serves as primary key
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

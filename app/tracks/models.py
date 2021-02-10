from django.db import models
import uuid


class Track(models.Model):
    # id field automatically added, serves as primary key
    # these properties map to database columns
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

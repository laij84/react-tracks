from django.db import models
import uuid
from users.models import User


class Track(models.Model):
    # id field automatically added, serves as primary key
    # these properties map to database columns
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    # cascade delete - if associated user is deleted, the track is also deleted
    # null=True = field is nullable by default, otherwise errors as existing entries don't have an associated user.
    posted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

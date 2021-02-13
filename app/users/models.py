import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Create a custom User model which extends the User from django's auth. 
    Do this to be able to override the id to be a UUID.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

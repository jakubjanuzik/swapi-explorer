from django.db import models


class Homeworld(models.Model):
    """Homeworld mapping from SWAPI."""

    url = models.URLField(unique=True)
    name = models.CharField(max_length=128)


class Collection(models.Model):
    """Collection model."""
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='csvs/')

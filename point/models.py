from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Point(models.Model):
    """Модель точек на карте"""
    name  = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.PointField(geography=True, srid=4326)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        index = [models.Index(fields=['location'])]

    def __str__(self):
        return self.name

class



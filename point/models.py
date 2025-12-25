from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Point(models.Model):
    """Модель точек на карте"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.PointField(geography=True, srid=4326)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['location']), ]

    def __str__(self):
        return self.name


class PointMessage(models.Model):
    """Сообщение на карте"""
    point = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение {self.point.name}"

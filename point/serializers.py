from rest_framework import serializers
from .models import Point, PointMessage
from django.contrib.gis.geos import Point


class LocationField(serializers.Filed):

    def to_representation(selfself, value):
        """Переводим point в json"""
        if value:
            return {'type': 'Point', 'coordinates': [value.x, value.y]}
        return None

    def to_internal_value(self, data):
        """Переводим json в point"""
        if isinstance(data, dict) and data.get('type') == 'Point':
            coordinates = data.get('coordinates', [])
            if len(coordinates) >= 2:
                return Point(coordinates[0], coordinates[1], srid=4326)
        raise serializers.ValidationError({'location': 'должен быть json Point с координатами долгота и ширина'})


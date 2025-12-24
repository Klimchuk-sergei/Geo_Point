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


class PointSerializer(serializers.ModelSerializer):
    """Сериализатор точек"""
    created_by = serializers.StringRelatedField(read_only=True)
    location = LocationField(read_only=True)

    class Meta:
        model = Point
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

        def create(self, validated_data):
            validated_data['created_by'] = self.context.get('request').user
            return super().create(validated_data)


class PointMessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений на точках"""
    user = serializers.StringRelatedField(read_only=True)
    point = serializers.PrimaryKeyRelatedField(queryset=Point.objects.all())

    class Meta:
        model = PointMessage
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PointSearchSerializer(serializers.Serializer):
    """Сериализатор для поиска точек"""
    latitude = serializers.FloatField(
        required=True,
        min_value=-90,
        max_value=90
    )
    longitude = serializers.FloatField(
        required=True,
        min_value=-180,
        max_value=180
    )
    radius = serializers.FloatField(
        required=True,
        min_value=0,
        help_text="Радиус в метрах"
    )

    def validate(self, data):
        """Создаем точку из координат"""
        data['location'] = Point(
            data['longitude'],
            data['latitude'],
            srid=4326
        )
        return data

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Point, PointMessage
from .serializers import (
    PointSerializer,
    PointMessageSerializer,
    PointSearchSerializer
)


class PointViewSet(viewsets.ModelViewSet):
    """вьюс для работы с точками"""
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Поиск точек по заданному радиусу"""
        serializer = PointSearchSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        location = data['location']
        radius = data['radius']

        points = Point.objects.filter(
            location__distance_lte=(location, D(m=radius)),
            created_by=request.user  # Фильтр по пользователю
        ).annotate(
            distance=Distance('location', location)
        ).order_by('distance')

        page = self.paginate_queryset(points)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(points, many=True)
        return Response(serializer.data)


class PointMessageViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с сообщениями точек"""
    queryset = PointMessage.objects.all()
    serializer_class = PointMessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Поиск сообщений в заданном радиусе"""
        serializer = PointSearchSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        location = data['location']
        radius = data['radius']

        # Поиск точек в радиусе
        points_in_radius = Point.objects.filter(
            location__distance_lte=(location, D(m=radius)),
            created_by=request.user
        )

        # Получаем сообщения для найденных точек
        messages = PointMessage.objects.filter(
            point__in=points_in_radius,
            user=request.user
        ).select_related('point')

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

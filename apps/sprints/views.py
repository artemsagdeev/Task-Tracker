from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsManager
from api.responses import success_response, error_response
from .models import Sprint
from .serializers import (
    SprintCreateUpdateSerializer,
    SprintListSerializer,
    SprintDetailSerializer
)

class SprintListCreateView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = Sprint.objects.select_related('project')
        user = self.request.user
        if user.is_manager():
            return queryset
        return queryset.filter(project__members=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SprintCreateUpdateSerializer
        return SprintListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsManager()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        sprint = serializer.save()
        return success_response(
            data=SprintDetailSerializer(sprint).data,
            message="Спринт создан",
            status_code=status.HTTP_201_CREATED
        )


class SprintDetailUpdateView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'put']

    def get_queryset(self):
        queryset = Sprint.objects.select_related('project')
        user = self.request.user
        if user.is_manager():
            return queryset
        return queryset.filter(project__members=user)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SprintCreateUpdateSerializer
        return SprintDetailSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsManager()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        sprint = serializer.save()
        return success_response(
            data=SprintDetailSerializer(sprint).data,
            message='Спринт изменён'
        )
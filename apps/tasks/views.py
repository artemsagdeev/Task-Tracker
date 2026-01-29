from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsManager
from api.responses import success_response, error_response
from .models import Task
from .filters import apply_task_filters
from .permissions import IsManagerOrDeveloper
from .services import can_change_status
from .serializers import (
    TaskCreateUpdateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
    TaskStatusUpdateSerializer,
    TaskAssignSerializer,
)


class TaskListCreateView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('assignee', 'sprint', 'sprint__project')
        if user.is_manager():
            return apply_task_filters(queryset, self.request.query_params)
        return apply_task_filters(
            queryset.filter(
                Q(assignee=user) | Q(sprint__project__members=user)
            ).distinct(), self.request.query_params
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskListSerializer

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
        task = serializer.save()
        return success_response(
            data=TaskDetailSerializer(task).data,
            message='Задание создано',
            status_code=status.HTTP_201_CREATED,
        )

class TaskDetailView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'put']

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsManager()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('assignee', 'sprint', 'sprint__project')
        if user.is_manager():
            return queryset
        return queryset.filter(
            Q(assignee=user) | Q(sprint__project__members=user)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskCreateUpdateSerializer
        return TaskDetailSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        task = serializer.save()
        return success_response(
            data=TaskDetailSerializer(task).data,
            message='Задание изменено',
        )

class TaskAssignView(generics.GenericAPIView):
    queryset = Task.objects.select_related('assignee', 'sprint', 'sprint__project')
    serializer_class = TaskAssignSerializer
    permission_classes = [IsManager]
    http_method_names = ['post']

    def post(self, request, pk):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        task.assignee = serializer.validated_data['user']
        task.save()
        return success_response(
            data=TaskDetailSerializer(task).data,
            message='Исполнитель успешно назначен',
        )

class TaskStatusUpdateView(generics.GenericAPIView):
    queryset = Task.objects.select_related('assignee', 'sprint', 'sprint__project')
    permission_classes = [IsManagerOrDeveloper]
    serializer_class = TaskStatusUpdateSerializer
    http_method_names = ['patch']

    def get_task(self, pk):
        user = self.request.user
        if user.is_manager():
            return get_object_or_404(self.queryset, pk=pk)
        queryset = self.queryset.filter(assignee=user)
        return get_object_or_404(queryset, pk=pk)

    def patch(self, request, pk):
        task = self.get_task(pk)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        new_status = serializer.validated_data['status']
        if not can_change_status(role=request.user.role, from_status=task.status, to_status=new_status):
            return error_response(
                code='INVALID_STATUS_TRANSITION',
                message='Нету допуска к изменению статуса',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        task.status = new_status
        task.save()
        return success_response(
            data=TaskDetailSerializer(task).data,
            message='Статус обновлён',
        )
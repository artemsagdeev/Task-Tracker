from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsManager
from api.responses import success_response, error_response
from .models import Project
from .serializers import (
    ProjectCreateUpdateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectAddMemberSerializer
)

User = get_user_model()

class ProjectListCreateView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = Project.objects.prefetch_related('members')
        user = self.request.user
        if user.is_manager():
            return queryset
        return queryset.filter(members=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateUpdateSerializer
        return ProjectListSerializer

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
        project = serializer.save()
        return success_response(
            data=ProjectDetailSerializer(project).data,
            message='Проект создан',
            status_code=status.HTTP_201_CREATED,
        )

class ProjectDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        queryset = Project.objects.prefetch_related('members')
        user = self.request.user
        if user.is_manager():
            return queryset
        return queryset.filter(members=user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectDetailSerializer
        return ProjectCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'DELETE'):
            return [IsManager()]
        return [IsAuthenticated()]

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
        project = serializer.save()
        return success_response(
            data=ProjectDetailSerializer(project).data,
            message='Задание изменено',
        )

class ProjectAddMemberView(generics.GenericAPIView):
    permission_classes = [IsManager]
    serializer_class = ProjectAddMemberSerializer
    http_method_names = ['post']

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data['user']
        if project.members.filter(id=user.id).exists():
            return error_response(
                code='VALIDATION_ERROR',
                message='Сотрудник уже является участником проекта',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        project.members.add(user)
        return success_response(
            data=ProjectDetailSerializer(project).data,
            message='Сотрудник добавлен в проект',
            status_code=status.HTTP_200_OK
        )

class ProjectRemoveMemberView(generics.GenericAPIView):
    permission_classes = [IsManager]
    http_method_names = ['delete']

    def delete(self, request, pk, user_id):
        project = get_object_or_404(Project, pk=pk)
        user = get_object_or_404(User, pk=user_id)
        if not project.members.filter(id=user.id).exists():
            return error_response(
                code='VALIDATION_ERROR',
                message='Сотрудник не является участником проекта',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        project.members.remove(user)
        return success_response(message='Сотрудник удалён с проекта')
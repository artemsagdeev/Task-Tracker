from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from api.enums import TaskStatus, UserRole
from apps.users.serializers import UserProfileSerializer
User = get_user_model()

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'status',
            'priority',
            'type'
        )

class TaskDetailSerializer(serializers.ModelSerializer):
    assignee = UserProfileSerializer(read_only=True)
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'type',
            'priority',
            'status',
            'assignee',
            'sprint',
            'created_at',
            'updated_at'
        )

class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=300)
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'type',
            'priority',
            'sprint'
        )

class TaskAssignSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=UserRole.DEVELOPER))

class TaskStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=TaskStatus.choices)


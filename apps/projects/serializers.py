from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project
from apps.users.serializers import UserProfileSerializer

User = get_user_model()


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'status'
        )

class ProjectDetailSerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'status',
            'members'
        )


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=300)
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'start_date',
            'end_date',
            'status',
        )

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date > end_date:
            raise serializers.ValidationError(
                'Дата начала не может быть позже даты окончания'
            )
        return attrs

class ProjectAddMemberSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
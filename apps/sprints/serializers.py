from rest_framework import serializers
from apps.projects.serializers import ProjectListSerializer
from .models import Sprint

class SprintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = (
            'id',
            'goal',
            'project'
        )

class SprintDetailSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True)
    class Meta:
        model = Sprint
        fields = (
            'id',
            'project',
            'start_date',
            'end_date',
            'goal'
        )

class SprintCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = (
            'project',
            'start_date',
            'end_date',
            'goal'
        )

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        project = attrs.get('project')

        if start_date > end_date:
            raise serializers.ValidationError(
                'Дата начала спринта должна быть раньше даты окончания спринта.'
            )

        if project:
            if start_date < project.start_date:
                raise serializers.ValidationError(
                    'Дата начала спринта не может быть раньше даты начала проекта.'
                )

            if end_date > project.end_date:
                raise serializers.ValidationError(
                    'Дата окончания спринта не может быть позже даты окончания проекта.'
                )

        return attrs


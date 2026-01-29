from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    TaskStatusUpdateView,
    TaskAssignView
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('tasks/<int:pk>/status/', TaskStatusUpdateView.as_view()),
    path('tasks/<int:pk>/assign/', TaskAssignView.as_view()),
]

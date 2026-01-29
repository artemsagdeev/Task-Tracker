from django.urls import path
from .views import (
    SprintListCreateView,
    SprintDetailUpdateView
)

urlpatterns = [
    path('sprints/', SprintListCreateView.as_view()),
    path('sprints/<int:pk>/', SprintDetailUpdateView.as_view())
]

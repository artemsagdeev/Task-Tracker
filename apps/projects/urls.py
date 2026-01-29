from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailUpdateDeleteView,
    ProjectAddMemberView,
    ProjectRemoveMemberView,
)

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view()),
    path('projects/<int:pk>/', ProjectDetailUpdateDeleteView.as_view()),
    path('projects/<int:pk>/members/', ProjectAddMemberView.as_view()),
    path('projects/<int:pk>/members/<int:user_id>/', ProjectRemoveMemberView.as_view()),
]

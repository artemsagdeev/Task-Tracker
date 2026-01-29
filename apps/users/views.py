from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.tasks.models import Task
from apps.tasks.serializers import TaskDetailSerializer
from api.responses import success_response, error_response
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    LoginSerializer,
    RefreshSerializer
)

User = get_user_model()

class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        return success_response(
            data={
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            message='Сотрудник зарегистрирован',
            status_code=status.HTTP_201_CREATED,
        )

class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='VALIDATION_ERROR',
                message='Данные введены неверно',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return error_response(
                code='INVALID_CREDENTIALS',
                message='Неверный пароль/имя сотрудника',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        return success_response(
            data={
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            message='Вход в систему прошел успешно',
        )

class RefreshView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='REFRESH_REQUIRED',
                message='Требуется токен обновления',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(serializer.validated_data['refresh'])
        except Exception:
            return error_response(
                code='INVALID_TOKEN',
                message='Недопустимый токен обновления',
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return success_response(
            data={
                'access': str(refresh.access_token)
            },
            message='Токен обновлён',
        )

class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code='REFRESH_REQUIRED',
                message='Требуется токен обновления',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(serializer.validated_data['refresh'])
        except Exception:
            return error_response(
                code='INVALID_TOKEN',
                message='Недопустимый токен обновления',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        refresh.blacklist()
        return success_response(message='Успешный выход из системы')

class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return success_response(data=serializer.data)

class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return success_response(data=serializer.data)

class MyTasksView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.select_related('assignee', 'sprint', 'sprint__project').filter(assignee=user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(data=serializer.data)

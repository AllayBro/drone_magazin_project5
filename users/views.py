from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, get_user_model

from .models import CustomUser
from drones.models import Drone, Booking
from .serializers import (
    DroneSerializer,
    BookingSerializer,
    UserSerializer,
    UserRegisterSerializer,
    LoginSerializer,
    UserProfileSerializer
)

User = get_user_model()


# 📦 Дроны
class DroneViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [permissions.AllowAny]


# 📅 Бронирования
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 👤 Только для админов (список пользователей)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


# 📝 Регистрация
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Пользователь зарегистрирован',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'token_type': 'Bearer'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔐 Логин по email
class EmailLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'token_type': 'Bearer'
        })


# ⚙️ Получение и обновление профиля пользователя
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]  # если нужен аватар

    def get_object(self):
        return self.request.user

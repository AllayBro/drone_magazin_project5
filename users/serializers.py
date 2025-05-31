from rest_framework import serializers
from django.contrib.auth import get_user_model
from drones.models import Drone, Booking
from .models import CustomUser

User = get_user_model()


# 🚁 Сериализатор дрона
class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'


# 📅 Сериализатор бронирования
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


# 👤 Сериализатор для админов (список пользователей)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'date_joined']


# 📝 Регистрация
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password', 'password2', 'role']  # ⛔ username убран

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)

        # 👇 Автогенерация username из email или nickname
        username = validated_data.get('nickname') or validated_data.get('email').split('@')[0]
        i = 1
        base_username = username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        return User.objects.create_user(
            username=username,  # ✅ сгенерированное
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname', ''),
            role=validated_data.get('role', 'user')
        )


# 🔐 Логин
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# ⚙️ Профиль пользователя (настройки)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'nickname', 'avatar', 'country', 'city', 'region')
        read_only_fields = ('id', 'username', 'email')

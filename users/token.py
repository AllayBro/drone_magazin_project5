from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    username_field = 'email'  # Обязательно для использования email вместо username

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны")

        user = authenticate(
            request=self.context.get("request"),
            email=email,  # здесь важно использовать кастомный backend, который работает с email
            password=password
        )

        if not user or not user.is_active:
            raise serializers.ValidationError("Неверный email или пароль")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'token_type': 'Bearer',
            'role': user.role  # Дополнено: роль для фронтенда
        }
        data = super().validate(attrs)
        data['role'] = user.role  # ДОБАВЬ ЭТУ СТРОКУ
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

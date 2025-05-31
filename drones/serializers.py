from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Drone, Booking

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone', 'avatar']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            avatar=validated_data.get('avatar')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'phone']


class DroneSerializer(serializers.ModelSerializer):
    currentPrice = serializers.SerializerMethodField()

    class Meta:
        model = Drone
        fields = '__all__'

    def get_currentPrice(self, obj):
        try:
            if obj.discount and isinstance(obj.discount, dict):
                if obj.discount.get("isActive") is True:
                    percentage = obj.discount.get("percentage", 0)
                    return round(obj.basePrice * (1 - percentage / 100))
            return obj.basePrice
        except Exception:
            return obj.basePrice


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    drone_name = serializers.CharField(source='drone.name', read_only=True)
    total_price = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            # drone можно оставить как есть, т.к. указываем явно
        }

    def get_total_price(self, obj):
        return obj.total_price

    def get_formatted_date(self, obj):
        return obj.formatted_date

    def get_formatted_time(self, obj):
        return obj.formatted_time


    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("User must be authenticated.")

        return super().create(validated_data)

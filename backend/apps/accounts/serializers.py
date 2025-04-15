from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, label="Повторите пароль")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        """
        Проверка, что введённые пароли совпадают.
        """
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        # Удаляем password2, т.к. он не нужен при создании объекта User
        validated_data.pop('password2')
        # Создаем пользователя через метод create_user (автоматически хеширует пароль)
        user = User.objects.create_user(**validated_data)
        return user
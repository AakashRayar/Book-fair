from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_password(self, value):
        # Ensure password meets strength requirements
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        # You can add further complexity checks here (uppercase, digits, special characters)
        return value

    def validate(self, data):
        # Ensure the password and confirm password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and confirm password do not match.")
        return data

    def create(self, validated_data):
        # Remove the confirm_password field before saving the user
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            # Use email to find the user
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Check if the password is correct
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        return {'user': user}
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserDetail


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for UserDetail model to handle user registration and validation.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserDetail
        fields = ['username', 'email', 'phone_number', 'bio', 'password']

    def validate(self, data):
        """
        Validate for duplicate username and combination of phone_number and email.
        """
        username = data.get('username')
        phone_number = data.get('phone_number')
        email = data.get('email')

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        # Check for duplicate phone number and email combination
        if UserDetail.objects.filter(phone_number=phone_number, email=email).exists():
            raise serializers.ValidationError(
                {"error": "User with this phone number and email already exists."}
            )

        return data

    def create(self, validated_data):
        """
        Create and return a new user with a UserDetail entry.
        """
        # Create the user first
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            defaults={
                'email': validated_data['email'],
                'password': validated_data['password']
            }
        )

        # Create or update UserDetail (if user already exists, update the details)
        user_detail, created = UserDetail.objects.update_or_create(
            user=user,
            defaults={
                'phone_number': validated_data['phone_number'],
                'bio': validated_data.get('bio', '')
            }
        )

        return user_detail

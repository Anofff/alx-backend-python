from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def validate_user_credentials(username, password):
    """
    Validate user credentials and return user if valid
    """
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid credentials")
    return user

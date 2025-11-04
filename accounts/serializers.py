from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from django.conf import settings


User = get_user_model()

# ------------------------------------------------------
# USER SERIALIZER
# ------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'handle', 'username', 'email')


# ------------------------------------------------------
# TOKEN SERIALIZER (JWT)
# ------------------------------------------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['is_active'] = user.is_active
        token['email_verified'] = user.email_verified

        # Attach basic profile info if it exists
        profile = getattr(user, 'profile', None)
        if profile:
            token['full_name'] = profile.full_name
            token['avatar'] = str(profile.avatar) if profile.avatar else None
        else:
            token['full_name'] = None
            token['avatar'] = None

        return token


# ------------------------------------------------------
# REGISTER SERIALIZER
# ------------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ------------------------------------------------------
# GOOGLE LOGIN SERIALIZER
# ------------------------------------------------------
class GoogleSocialAuthSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            # Validate Google token
            audience = getattr(settings, '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', None)
            if not audience:
                raise serializers.ValidationError("Google Sign-In not configured on server.")
            idinfo = id_token.verify_oauth2_token(
                value,
                google_requests.Request(),
                audience=audience
            )

            email = idinfo.get('email')
            User = get_user_model()

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'is_active': True
                }
            )
            self.context['user'] = user
            return value

        except ValueError:
            raise serializers.ValidationError("Invalid or expired token.")

    def create(self, validated_data):
        return self.context['user']


# ------------------------------------------------------
# CHANGE PASSWORD SERIALIZER
# ------------------------------------------------------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# ------------------------------------------------------
# PROFILE SERIALIZER
# ------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'full_name',
            'phone_number',
            'date_of_birth',
            'avatar',
            'bio',
            'occupation',
            'interests',
        )

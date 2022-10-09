import random
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from jwt.utils import force_bytes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['phone', 'firstName', 'lastName', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password & Confirm Password are not same')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserOtpVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    class Meta:
        model = User

    def validate(self, attrs):
        try:
            otp = attrs.get('otp')
            uEid = self.context.get('uid')
            token = self.context.get('token')
            uid = urlsafe_base64_decode(uEid)
            user = User.objects.filter(id=uid)

            if not user.exists():
                raise serializers.ValidationError('User Not Found')
            else:
                user = user[0]

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Your Session Time is Expired')
            if otp != user.otp:
                raise ValidationError('Wrong OTP')
            if user.is_active:
                raise ValidationError('User Already Created')

            user.is_active = True
            user.save()
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired')
            pass

        return attrs

class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['phone', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'firstName', 'lastName']

class ChangeUserPasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password & Confirm Password are not same')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['phone']

    def validate(self, attrs):
        phone = attrs.get('phone')

        if not User.objects.filter(phone = phone, is_active = True).exists():
            raise serializers.ValidationError("You is not a Registered User")
        return attrs

class UserPasswordResetSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            otp = attrs.get('otp')
            uEid = self.context.get('uid')
            token = self.context.get('token')
            uid = urlsafe_base64_decode(uEid)
            user = User.objects.filter(id=uid)
            if not user.exists():
                raise serializers.ValidationError('User Not Found')
            else:
                user = user[0]
            if password != password2:
                raise serializers.ValidationError('Password & Confirm Password are not same')
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Your Session Time is Expired')
            if otp != user.otp:
                raise ValidationError('Wrong OTP')

            user.set_password(password)
            user.save()
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired')
            pass

        return attrs

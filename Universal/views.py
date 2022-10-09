import random
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from django.contrib.auth import authenticate
from .renderers import *
import os
from twilio.rest import Client
from MB_Settings import settings

# Twillo Client
client = Client(settings.TWILLO_ACCOUNT_SID, settings.TWILLO_AUTH_TOKEN)

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializers = UserRegistrationSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):

            # request data
            phone = serializers.validated_data.get('phone')
            firstName = serializers.validated_data.get('firstName')
            lastName = serializers.validated_data.get('lastName')
            password = serializers.validated_data.get('password')
            otp = random.randint(1001, 9999)

            userObjects = User.objects.filter(phone = phone)

            if userObjects.exists():
                user = userObjects[0]
                if not user.is_active:
                    user.phone = phone
                    user.firstName = firstName
                    user.lastName = lastName
                    user.otp = otp
                    user.set_password(password)
                    user.save()
                    uEid = urlsafe_base64_encode(force_bytes(str(user.id)))
                    OTPtoken = PasswordResetTokenGenerator().make_token(user)
                    link = "http://localhost:8000/user/verify-user/{}/{}/".format(uEid, OTPtoken)
                    message = client.messages \
                        .create(
                        body='Hi {} {},\n\nYour OTP is {}\nThis OTP Expire After 5 Minutes Do Not Share With anyone\n\nYour Sincerely\nMaintain Book.'.format(firstName, lastName, otp),
                        from_=settings.TWILLO_PHONE_NUMBER,
                        to='+91{}'.format(phone)
                    )
                    return Response({'msg': 'Registration Successful', 'url':link, 'otpStatus':message.sid}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'errors': {'non_field_errors': ['User already Exist']}}, status=status.HTTP_403_FORBIDDEN)
            else:
                user = serializers.save()
                uEid = urlsafe_base64_encode(force_bytes(str(user.id)))
                OTPtoken = PasswordResetTokenGenerator().make_token(user)
                link = "http://localhost:8000/user/verify-user/{}/{}/".format(uEid, OTPtoken)
                message = client.messages \
                    .create(
                    body='Hi {} {},\n\nYour OTP is {}\nThis OTP Expire After 5 Minutes. Do Not Share With anyone\n\nYour Sincerely\nMaintain Book.'.format(
                        user.firstName, user.lastName, user.otp),
                    from_=settings.TWILLO_PHONE_NUMBER,
                    to='+91{}'.format(user.phone)
                )
                return Response({'msg':'Registration Successful', 'url':link, 'otpStatus':message.sid}, status = status.HTTP_201_CREATED)

        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)


class UserOtpVerificationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uEid, token, format=None):
        serializer = UserOtpVerificationSerializer(data=request.data, context={'uid':uEid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            uid = urlsafe_base64_decode(uEid)
            user = User.objects.filter(id = uid)
            if user.exists():
                token = get_tokens_for_user(user[0])
                return Response({'msg':'User Activation Sucessfully', 'token':token},
                                status = status.HTTP_200_OK)
            else:
                return Response({'msg':'User Not Found'}, status = status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializers = UserLoginSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            phone = serializers.data.get('phone')
            password = serializers.data.get('password')
            user = authenticate(phone=phone, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg':'Login Successful', 'token':token}, status = status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializers = UserProfileSerializer(request.user)
        return Response(serializers.data, status = status.HTTP_200_OK)

class ChangeUserPasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ChangeUserPasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Sucessfully'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(phone = serializer.validated_data.get('phone'))
            uEid = urlsafe_base64_encode(force_bytes(str(user.id)))
            token = PasswordResetTokenGenerator().make_token(user)
            user.otp = random.randint(1001, 9999)
            user.save()
            link = "http://localhost:8000/user/reset-password/{}/{}/".format(uEid, token)
            message = client.messages \
                .create(
                body='Hi {} {},\n\nYour OTP is {}\nThis OTP Expire After 5 Minutes\nDo Not Share With anyone\n\nYour Sincerely\nMaintain Book.'.format(
                    user.firstName, user.lastName, user.otp),
                from_=settings.TWILLO_PHONE_NUMBER,
                to='+91{}'.format(user.phone)
            )
            return Response({'msg':'Password Reset link send. Please check your Messages', 'url':link, 'otpStatus':message.sid}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uEid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uEid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Sucessfully'},
                            status = status.HTTP_200_OK)

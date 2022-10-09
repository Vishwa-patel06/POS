import random
import jwt
from MB_Settings import settings
from rest_framework import authentication
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from jwt.utils import force_bytes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
import re

class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ['firstName', 'lastName', 'gstNumber', 'contactNumber', 'contactEmail', 'customerWebsite', 'address', 'pincode', 'town', 'state', 'district']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        gstNumber = attrs.get('gstNumber')
        regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$"

        p = re.compile(regex)

        if gstNumber != None:
            if not (re.search(p, gstNumber)):
                raise serializers.ValidationError('GST Number is not valid')

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        auth = authentication.get_authorization_header(request).split()
        token = auth[1].decode()
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        uid = decoded['user_id']
        user_obj = User.objects.get(id=uid)
        validated_data['userObject']  = user_obj
        return CustomerModel.objects.create(**validated_data)

class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = '__all__'

from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import CustomerRenderer
from .serializer import *
# Create your views here.

class CustomerRegistrationView(APIView):
    renderer_classes = [CustomerRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializers = CustomerCreateSerializer(data=request.data, context={'request':request})
        if serializers.is_valid(raise_exception=True):
            customer = serializers.save()
            return Response({"msg":"Customer Sucessfully Created"}, status = status.HTTP_201_CREATED)

        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)


class CustomerListView(APIView):
    renderer_classes = [CustomerRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        auth = authentication.get_authorization_header(request).split()
        token = auth[1].decode()
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        uid = decoded['user_id']
        user_obj = User.objects.get(id=uid)
        customerObjects = CustomerModel.objects.filter(userObject = user_obj)
        serializers = CustomerListSerializer(customerObjects, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
        # return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

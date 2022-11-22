from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer
from rest_framework import response, status
from drf_yasg.utils import swagger_auto_schema



class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer
    @swagger_auto_schema(operation_description="register")
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


registerView = RegisterApiView.as_view()

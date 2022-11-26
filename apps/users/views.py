import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.tasks import send_email

from .models import User
from .serializers import (
    EmailVerificationSerializer,
    LoginSerializer,
    RegisterSerializer,
)


class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse("email-verify")
        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.username
            + " Use the link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        send_email.delay(data)
        return response.Response(user_data, status=status.HTTP_201_CREATED)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_description="login")
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(
            {"message": "Invalid Credentials, try again!"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return response.Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return response.Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


###############
registerView = RegisterApiView.as_view()
loginView = LoginApiView.as_view()
verifyView = VerifyEmailView.as_view()

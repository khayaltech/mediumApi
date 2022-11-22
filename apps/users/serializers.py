from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    """This class will be used for registration"""

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        "username": "The username should only contain alphanumeric characters"
    }

    class Meta:
        """Initializing fields and model"""

        model = User
        fields = ["email", "username","first_name", "last_name", "password"]

    def validate(self, attrs):
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

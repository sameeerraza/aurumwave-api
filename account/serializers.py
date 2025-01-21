from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import EndUser


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["is_portal_admin"] = user.is_portal_admin
        token["name"] = user.name

        return token


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = EndUser
        fields = ("username", "email", "password", "phone", "country")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class EndUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = EndUser
        fields = [
            "username",
            "email",
            "name",
            "phone",
            "country",
            "city"
        ]

    # def validate_password(self, value):
    #     self.instance.set_password(value)
    #     return self.instance.password

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "first_name", "last_name",'password', 'photo', 'venndor_authorized', 'profil_type', 'gender','phone_number']
        extra_kwargs = {'confirm_password': {'write_only': True}, 'password': {'write_only': True}}



class UserEssentialSerializer(serializers.ModelSerializer):
    #store = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "profil_type"

            #"store",
        ]

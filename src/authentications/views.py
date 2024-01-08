from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


from agrijeune.exceptions import (
    UserNotFoundError,
    VendorNotAuthorizedError,
    ClientNotAuthorizedError
)
from .models import User
from .serialiser import UserSerializer, UserEssentialSerializer


def verify_email(email):
    try:
        validate_email(email)
        return False
    except ValidationError:
        return True


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Vérifier la correspondance des mots de passe
            password = serializer.validated_data['password']
            confirm_password = request.data.get('confirm_password')
            profil = request.data.get('profil_type')
            if profil.lower() in ['client', 'agripreneur', 'commerçant']:
                if password == confirm_password:
                    # Hacher le mot de passe avant de l'enregistrer dans la base de données
                    user = serializer.save()
                    if user.is_client():
                        user.is_active = True
                    user.set_password(password)
                    user.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Les mots de passe ne correspondent pas.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Le profil doit etre un client ou un agripreneur/commerçant.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if verify_email(username) == True:
        # Authentification avec le courriel ou le nom d'utilisateur
            user = User.objects.filter(username=username).first()
        else:
            user = User.objects.filter(email=username).first()

        
            
        if user is None:
            raise UserNotFoundError()
        if user.is_vendor():
            print(user.is_vendor())
            raise VendorNotAuthorizedError()
        elif user.check_password(password ):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user_essential_serializer = UserEssentialSerializer(user)
            data = {
                "refresh": str(refresh),
                "access_token": access_token,
                "code": 1,
                "status": status.HTTP_200_OK,
                "user": user_essential_serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)



class LoginVendorView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if verify_email(username):
        # Authentification avec le courriel ou le nom d'utilisateur
            user = User.objects.filter(username=username).first()
        else:
            user = User.objects.filter(email=username).first()

        if user is None:
            raise UserNotFoundError()
        elif user.is_client():
            raise ClientNotAuthorizedError()
        elif user.venndor_authorized == False:
            return Response({'error': "Veuillez contacter l'admin"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user.check_password(password ):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user_essential_serializer = UserEssentialSerializer(user)
            data = {
                "refresh": str(refresh),
                "access_token": access_token,
                "code": 1,
                "status": status.HTTP_200_OK,
                "user": user_essential_serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Révocation du jeton d'accès (Blacklisting)
            refresh_token = request.data.get('refresh_token')
            RefreshToken(refresh_token).blacklist()
            return Response({'detail': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
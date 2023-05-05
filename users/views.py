from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AppUserToken, User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name =  serializer.validated_data['first_name']
            last_name =  serializer.validated_data['last_name']
            gender =  serializer.validated_data['gender']
            user = User(email=email,first_name =first_name, last_name= last_name, gender= gender, is_active = True)
            user.set_password(password)
            user.save()
            return Response({'message': 'User created successfully'})
        return Response(serializer.errors, status=400)




class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            token, created = AppUserToken.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

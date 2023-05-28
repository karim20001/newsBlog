from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.generics import GenericAPIView
from django.contrib.auth import login, logout
from rest_framework import generics

from members.serializers import UserSignUpSerializers, UserLoginSerializer

class UserSignUpViewSet(generics.CreateAPIView):

    # queryset = User.objects.all().order_by('-date_joined')
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data) 

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            messgae = f'hello{username}'
            serializer.save()
            return Response({'message': messgae}, status.HTTP_201_CREATED)
        
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    # permission_classes = [permissions.IsAuthenticated]

class UserLoginApiView(GenericAPIView):

    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status.HTTP_202_ACCEPTED)
        # if serializer.is_valid():
        #     user = serializer.get_user()
        #     login(request, user)
        #     return Response({'message': 'd'}, status.HTTP_202_ACCEPTED)
        
        # return Response("", status.HTTP_400_BAD_REQUEST)

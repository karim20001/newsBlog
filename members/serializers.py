from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator

class UserSignUpSerializers(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    confirm_password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        password = attrs.get('password')
        conf_pass = attrs.pop('confirm_password')
        if password != conf_pass:
            raise serializers.ValidationError()
        return attrs
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "confirm_password",)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'confirm_password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password'],
            # confirm_password = validated_data['confirm_password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        # label="نام کاربری"
        write_only=True,
    )

    password = serializers.CharField(
        # lable="رمز",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
            
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    

    # @classmethod
    # def get_token(cls, user):
    #     token = super()
    # class Meta:
    #     model = User
    #     fields = ('username', 'password')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['placeholder'] = 'نام کاربری'
    #     self.fields['password'].widget.attrs['placeholder'] = 'رمز'
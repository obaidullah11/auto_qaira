# from rest_framework import serializers
from django.contrib.auth import authenticate













from rest_framework import serializers
from users.models import User 

class UserProfileSerializernew(serializers.ModelSerializer):
    # Return both refresh and access JWT tokens
    # tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            # Primary key
            'id',

            # Identity
            'email',
            'username',
           

           

            # Roles & flags
            'profile_pic',
            'user_type',
            'is_admin',
            'about_yourself',
            'address',
            'mobile',
            'is_approved',
            'is_deleted',
            'is_mute',

            # Device
      

            # Tokens
            
        ]
       

    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'profile_pic', 'about_yourself',
            'address', 'mobile'
        ]
    

from rest_framework import serializers
from users.models import User 

class UserProfileSerializer(serializers.ModelSerializer):
    # Return both refresh and access JWT tokens
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            # Primary key
            'id',

            # Identity
            'email',
            'username',
            
            # Roles & flags
            'profile_pic',
            'user_type',
            

            # Device
          

            # Tokens
            'tokens',
        ]
        read_only_fields = ('id', 'tokens')

    def get_tokens(self, obj):
        """
        Delegates to your model’s `get_jwt_token()`,
        which returns {'refresh': ..., 'access': ...}.
        """
        return obj.get_jwt_token()

    def update(self, instance, validated_data):
        """
        Apply any writable fields and save.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

#
#import logging
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import logging
User = get_user_model()
logger = logging.getLogger(__name__)
import random
from django.core.mail import send_mail
from django.conf import settings
class RegisterUserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPES, default='customer')
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password', 
            'user_type', 'is_approved', 'is_deleted',
            'is_mute', 'tokens', 'otp', 'is_email_verified',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'id': {'read_only': True},
            'username': {'required': False},
            'otp': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("This email is already taken.")
        return email

    def generate_otp(self):
        return str(random.randint(1000, 9999))

    def send_otp_email(self, user):
        subject = 'Complete Your  Auto Qira Account Creation'
        message = f'''Dear User,

        We received a request to create your account on Auto Qira.

        Your One-Time Password (OTP) is: {user.otp}

        Please use this OTP to complete your account creation process. If you did not request an OTP for account creation, please ignore this message.

        Thank you,
        The Auto Qira Team
        '''
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    @transaction.atomic
    def create(self, validated_data):
        logger.debug("Creating user with data: %s", {k: v for k, v in validated_data.items() if k != 'password'})
        password = validated_data.pop('password')
        otp = self.generate_otp()
        validated_data['otp'] = otp

        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=password,
            **{k: v for k, v in validated_data.items() if k not in ('email', 'username')}
        )

        self.send_otp_email(user)
        logger.info("User created and OTP sent to: %s", user.email)
        return user

    def get_tokens(self, obj):
        return obj.get_jwt_token()

    
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email').strip().lower()
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials."})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is disabled."})
        tokens = user.get_jwt_token()
        attrs['access'] = tokens.get('access')
        attrs['refresh'] = tokens.get('refresh')
        attrs['user'] = user
        return attrs
# import string
# import random
# from django.contrib.auth.hashers import make_password
# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class SocialRegistrationSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
#     last_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
#     email = serializers.EmailField(max_length=254, required=True)
#     profile_pic_url = serializers.URLField(required=False, allow_blank=True)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'profile_pic_url']

#     def generate_random_password(self, length=12):
#         characters = string.ascii_letters + string.digits + string.punctuation
#         return ''.join(random.choices(characters, k=length))

#     def create(self, validated_data):
#         email = validated_data.get('email')
#         first_name = validated_data.get('first_name', '').strip()
#         last_name = validated_data.get('last_name', '').strip()
#         profile_pic_url = validated_data.get('profile_pic_url', '')

#         base_username = f"{first_name}{last_name}".lower() if first_name or last_name else email.split('@')[0]
#         username = base_username
#         counter = 1
#         while User.objects.filter(username=username).exists():
#             username = f"{base_username}{counter}"
#             counter += 1

#         random_password = self.generate_random_password()

#         user, created = User.objects.get_or_create(email=email, defaults={
#             'first_name': first_name,
#             'last_name': last_name,
#             'profile_pic_url': profile_pic_url,
#             'username': username,
#             'password': make_password(random_password)
#         })

#         if not created:
#             user.first_name = first_name
#             user.last_name = last_name
#             user.profile_pic_url = profile_pic_url
#             if not user.username:
#                 user.username = email
#             user.save()

#         return user



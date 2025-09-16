from rest_framework import serializers
from .models import CustomUser, OTP, UserProfile
from django.contrib.auth import get_user_model, authenticate
from payment.models import Subscription
from notifications.models import Notification
User = get_user_model()

from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()
 
   
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role', 'is_verified', 'user_profile']
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser', 'role']

    def get_user_profile(self, obj):
        try:
            profile = obj.user_profile
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None

    

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES, default='user')
    farm_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'name', 'farm_name']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}
        }

    def validate(self, data):
        errors = {}
        if not data.get('email'):
            errors['email'] = ['This field is required']
        if not data.get('password'):
            errors['password'] = ['This field is required']
        if not data.get('name'):
            errors['name'] = ['This field is required']

        # Check if verified user already exists
        if data.get('email') and User.objects.filter(email=data['email'], is_verified=True).exists():
            errors['email'] = ['A user with this email already exists']

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        name = validated_data.pop('name')
        farm_name = validated_data.pop('farm_name', None)  # safe pop

        # Check if unverified user exists
        user = User.objects.filter(email=validated_data['email'], is_verified=False).first()

        if user:
            # Update the existing unverified user
            user.set_password(validated_data['password'])
            user.role = validated_data.get('role', 'user')
            user.save()
        else:
            # Create new user if not found
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                role=validated_data.get('role', 'user')
            )

        # Create or update profile
        if user.role == "farm":
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"name": name, "farm_name": farm_name}
            )
        else:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"name": name}
            )

        # Always send notification
        Notification.objects.create(
            user=user,
            title="New User Registration",
            message=f"A new {user.role} has registered your platform: {name} ({user.email})",
            notification_type="user_management"
        )

        return user


class OTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    class Meta:
        model = OTP
        fields = ['id', 'email', 'otp', 'created_at', 'attempts']
        read_only_fields = ['id', 'created_at', 'attempts']

    def validate(self, data):
        errors = {}
        if not data.get('email'):
            errors['email'] = ['This field is required']
        if not data.get('otp'):
            errors['otp'] = ['This field is required']
        if errors:
            raise serializers.ValidationError(errors)
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'profile_picture', 'phone_number', 'joined_date']
        read_only_fields = ['id', 'user', 'joined_date']

    def validate(self, data):
        errors = {}
        if 'name' in data and not data['name']:
            errors['name'] = ['Name cannot be empty']
        if errors:
            raise serializers.ValidationError(errors)
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        errors = {}
        email = data.get('email')
        password = data.get('password')

        if not email:
            errors['email'] = ['This field is required']
        if not password:
            errors['password'] = ['This field is required']
        if errors:
            raise serializers.ValidationError(errors)

        user = authenticate(email=email, password=password)
        if not user:
            errors['credentials'] = ['Invalid email or password']
            raise serializers.ValidationError(errors)
        if not user.is_active:
            errors['credentials'] = ['Account not verified. Please verify your email with the OTP sent']
            raise serializers.ValidationError(errors)
        return user
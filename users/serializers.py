from rest_framework import serializers
from .models import User
from .utils import generate_random_username, generate_random_password

class UserSerializer(serializers.ModelSerializer):
    generated_password = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    # password field is removed from explicit definition, it's handled in create

    class Meta:
        model = User
        fields = ('id', 'email', 'user_type', 'username', 'generated_password')

    def create(self, validated_data):
        email = validated_data['email']
        email_prefix = email.split('@')[0]

        generated_username = generate_random_username(email_prefix)
        if generated_username is None:
            raise serializers.ValidationError(
                {"detail": "Could not generate a unique username. Please try a different email or contact support."}
            )

        raw_password = generate_random_password()

        user = User.objects.create_user(
            username=generated_username,
            email=email, # Use the email from validated_data directly
            password=raw_password, # Pass the raw password to create_user
            user_type=validated_data.get('user_type', 'client')
        )
        # Store the raw password on the serializer instance to pass to to_representation
        self.generated_password_value = raw_password
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Add the generated_password to the output
        if hasattr(self, 'generated_password_value'):
            ret['generated_password'] = self.generated_password_value

        # Ensure the actual password hash is not part of the response
        # The 'password' field is not in Meta.fields for output anymore,
        # but this is an extra safeguard if super() included it for some reason.
        ret.pop('password', None)
        return ret

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # For now, we are not adding any custom claims or overriding validate,
    # as Django's last_login is updated by the authenticate() call
    # made by TokenObtainPairView.
    # This class serves as a placeholder for future customizations if needed.
    pass

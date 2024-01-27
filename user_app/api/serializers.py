from django.contrib.auth.models import User 
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style ={'input_style': 'password'}, write_only = True)
    class Meta:
        model = User 
        fields = ("email", "username", "password", "password2")
        extra_kwargs = {
            "password": {'write_only': True}
        }
    
    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['password2']
        email = self.validated_data['email']
        username = self.validated_data['username']
        if password != confirm_password:
            raise serializers.ValidationError({
                "error": "The 2 passwords should be equal"
            })
        
        if User.objects.filter(email= email).exists():
            raise serializers.ValidationError({
                "error": "Email already registered"
            })

        account = User(
            email = email,
            username = username,
        )
        account.set_password(password)

        account.save()
        return account
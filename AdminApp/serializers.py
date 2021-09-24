from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class UserViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields ='__all__'
        
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','ROLE')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
    def validate_email(self, value):
        user = self.context['request'].user
        print(user)
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.username = validated_data['ROLE']
        

        instance.save()

        return instance
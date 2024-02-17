from rest_framework import serializers
from .models import Student, StudentSummary, Product, FuturePlan
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FuturePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuturePlan
        fields = '__all__'

class StudentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSummary
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = StudentSerializer(instance.student).data
        return representation
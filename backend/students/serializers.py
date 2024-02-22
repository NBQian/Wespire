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
    pdf_file_url = serializers.SerializerMethodField()

    class Meta:
        model = StudentSummary
        fields = '__all__'
    def get_pdf_file_url(self, obj):
        # This method will be called for each instance being serialized
        if obj.pdf_file:
            # Print the URL for debugging purposes
            print(obj.pdf_file.url)
            print(obj.pdf_file)
            print(obj.pdf_file.name)
            return obj.pdf_file.url
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = StudentSerializer(instance.student).data
        return representation
import os
from django.utils import timezone
from rest_framework import viewsets
from .models import Student, StudentSummary, Product, FuturePlan
from .serializers import StudentSerializer, StudentSummarySerializer, ProductSerializer, FuturePlanSerializer
from .utils import generate_pdf
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.conf import settings
from django.core.files import File




class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StudentSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentSummary.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        student_summary = serializer.save(date_created=timezone.now())
        pdf_file = generate_pdf(student_summary, student_summary.student.DateOfBirth)

        student_summary.pdf_file.save(pdf_file.name, pdf_file, save=True)

    def perform_update(self, serializer):
        updated_summary = serializer.save(date_created=timezone.now())

        # Check and delete the old PDF file
        if updated_summary.pdf_file:
            updated_summary.pdf_file.delete(save=False)

        # Generate a new PDF
        pdf_file = generate_pdf(updated_summary, updated_summary.student.DateOfBirth)
        updated_summary.pdf_file.save(pdf_file.name, pdf_file, save = True)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    def get_queryset(self):
        queryset = Product.objects.all()
        unique_code = self.request.query_params.get('unique_code', None)
        if unique_code is not None:
            queryset = queryset.filter(unique_code=unique_code)
        return queryset
    

class FuturePlanViewSet(viewsets.ModelViewSet):
    serializer_class = FuturePlanSerializer
    permission_classes = [IsAuthenticated]
    queryset = FuturePlan.objects.all()
    def get_queryset(self):
        queryset = FuturePlan.objects.all()
        unique_code = self.request.query_params.get('unique_code', None)
        if unique_code is not None:
            queryset = queryset.filter(unique_code=unique_code)
        return queryset

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class BaseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        index_file_path = os.path.join(settings.BASE_DIR, 'build', 'index.html')
        return FileResponse(open(index_file_path, 'rb'), content_type='text/html')
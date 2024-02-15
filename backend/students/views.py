import os
from django.utils import timezone
from rest_framework import viewsets
from .models import Student, StudentSummary, Product, FuturePlan
from .serializers import StudentSerializer, StudentSummarySerializer, ProductSerializer, FuturePlanSerializer
from .utils import generate_pdf
from rest_framework.permissions import IsAuthenticated


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
        pdf_file_path = generate_pdf(student_summary, self.request.user)
        student_summary.pdf_file = pdf_file_path
        student_summary.save()

    def perform_update(self, serializer):
        updated_summary = serializer.save(date_created=timezone.now())

        # Check and delete the old PDF file
        if updated_summary.pdf_file:
            if os.path.isfile(updated_summary.pdf_file.path):
                os.remove(updated_summary.pdf_file.path)

        # Generate a new PDF
        pdf_file_path = generate_pdf(updated_summary, self.request.user)
        updated_summary.pdf_file = pdf_file_path

        # Now save the instance to the database
        updated_summary.save()

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


import datetime, os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')
    studentId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    RegistrationNo = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Course = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15, null = True, blank = True)


class StudentSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='summaries')
    unique_code = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    pdf_file = models.FileField(upload_to='client_summaries/', blank=True, null=True)
    # agent name

    def delete(self, *args, **kwargs):
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):
                os.remove(self.pdf_file.path)
        super(StudentSummary, self).delete(*args, **kwargs)


class Product(models.Model):
    unique_code = models.CharField(max_length=255)
    Company = models.CharField(max_length=100)
    ProductNumber = models.CharField(max_length=100)
    ProductName = models.CharField(max_length=100)
    Date = models.DateField()
    Type = models.CharField(max_length=100)
    WholeLife = models.DecimalField(max_digits=10, decimal_places=2)
    Endowment = models.DecimalField(max_digits=10, decimal_places=2)
    Term = models.DecimalField(max_digits=10, decimal_places=2)
    InvLinked = models.DecimalField(max_digits=10, decimal_places=2)
    TotalDeathCoverage = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPermanentDisability = models.DecimalField(max_digits=10, decimal_places=2)
    EarlyCriticalIllness = models.DecimalField(max_digits=10, decimal_places=2)
    Accidental = models.DecimalField(max_digits=10, decimal_places=2)
    OtherBenefitsRemarks = models.TextField()
    Mode = models.CharField(max_length=100)
    Monthly = models.DecimalField(max_digits=10, decimal_places=2)
    Quarterly = models.DecimalField(max_digits=10, decimal_places=2)
    SemiAnnual = models.DecimalField(max_digits=10, decimal_places=2)
    Yearly = models.DecimalField(max_digits=10, decimal_places=2)
    MaturityPremiumEndDate = models.CharField(max_length=100)
    CurrentValue = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPremiumsPaid = models.DecimalField(max_digits=10, decimal_places=2)

class FuturePlan(models.Model):
    unique_code = models.CharField(max_length=255)
    Type = models.CharField(max_length=100)
    CurrentSumAssured = models.DecimalField(max_digits=10, decimal_places=2)
    RecommendedSumAssured = models.DecimalField(max_digits=10, decimal_places=2)
    Shortfall = models.DecimalField(max_digits=10, decimal_places=2)
    Remarks = models.TextField()

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

        
    
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email
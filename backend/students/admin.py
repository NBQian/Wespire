from django.contrib import admin
from .models import Student

models_list = [Student]
admin.site.register(models_list)

from django.contrib import admin
from .models import UserAccount
from .models import Student, UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_staff', 'is_active', 'is_superuser']
    search_fields = ['email', 'name']
    readonly_fields = []

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


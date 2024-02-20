from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentSummaryViewSet, ProductViewSet, FuturePlanViewSet
from .views import BaseView
# Create a router and register our viewsets with it.
router = DefaultRouter()

# Specify the basename argument for each viewset
router.register(r'clients', StudentViewSet, basename='client')
router.register(r'client-summaries', StudentSummaryViewSet, basename='client-summaries')
router.register(r'products', ProductViewSet, basename = 'product')
router.register(r'future-plans', FuturePlanViewSet, basename = 'futureplan')

# The API URLs are now determined automatically by the router.
urlpatterns = [
	path('', BaseView.as_view(), name='base-url'),
    path('', include(router.urls)),
]

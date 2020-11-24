from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path('api/data_to_real_estate_website/', data_to_real_estate_website.as_view(), name='data_to_real_estate_website'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
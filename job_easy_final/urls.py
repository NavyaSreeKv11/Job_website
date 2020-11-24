"""job_easy_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
path('',include(('job_easy.urls','job_easy'),namespace="job_easy")),
path('',include(('employee_app.urls','employee_app'),namespace="employee_app")),
path('',include(('employer_app.urls','employer_app'),namespace="employer_app")),

path('',include(('data_service.urls','data_service'),namespace="data_service")),
path('',include(('statistics_and_service.urls','statistics_and_service'),namespace="statistics_and_service")),
path('',include(('recruiter_service.urls','recruiter_service'),namespace="recruiter_service")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from .views import post_a_job,job_data,post_an_application
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/job_data',job_data.as_view()),
    path('api/post_a_new_job',post_a_job.as_view()),
    path('api/post_an_application', post_an_application.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
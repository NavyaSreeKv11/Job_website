from .views import *
from django.urls import path

urlpatterns = [
                path('employer/home/', home, name='home'),
                path('employer/add_job/', add_job_post, name='add_job_post'),
                path('employer_profile/', employer_profile_page, name='employer_profile_page'),
                path('employer_edit/', employer_edit_page, name='employer_edit_page'),
                path('employer/view_jobs/', emp_job_listing, name='emp_job_listing'),
                path('employer/view_applicants/', applicants_page, name='applicants_page'),
                path('delete/', job_delete, name='job_delete'),
                path('update_app_status_to_select/', update_app_status_to_select, name='update_app_status_to_select'),
                path('update_app_status_to_reject/', update_app_status_to_reject, name='update_app_status_to_reject'),
                path('update_app_status_to_delete/', update_app_status_to_delete, name='update_app_status_to_delete'),

]

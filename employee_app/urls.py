from .views import *
from django.urls import path

urlpatterns = [
                path('employee_profile/', employee_profile_page, name='employee_profile'),
                path('employee_edit/', employee_edit_page, name='employee_edit_page'),
                path('employee_history_jobs/', View_history_jobs, name='View_history_jobs'),
                path('employee_applied_jobs/', View_applied_jobs, name='View_applied_jobs'),
                path('employee_rateJob/', RateJob, name='RateJob'),
                path('saved_jobs/', saved_jobs, name='saved_jobs'),
                path('employee/save_job/', save_job, name='save_job'),
                path('view_job/', view_job, name='view_job'),
                path('apply_job/', apply_job, name='apply_job'),
                path('employee/job_applied/', View_applied_jobs, name='View_applied_jobs'),

]
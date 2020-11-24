from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(employee_profile)
admin.site.register(employer_profile)
admin.site.register(job)
admin.site.register(application)
admin.site.register(savedjobs)
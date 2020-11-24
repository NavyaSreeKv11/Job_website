from job_easy.models import job, application,User,employer_profile,employee_profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import data_to_real_estate_website_Serializer

class data_to_real_estate_website(APIView):

    def get(self,request):
        params={}

        jobs=job.objects.all()
        job_details=[]
        for each in jobs:
            job_type=each.job_type
            job_details.append({job_type:each.job_address})

        application_details=[]
        applications=application.objects.all()
        for each in applications:
            job_type=each.job.job_type
            application_details.append({job_type:each.job.job_address})

        worker_details = []
        applications = application.objects.all()
        for each in applications:
            job_type = each.job.job_type
            try:
                worker_details.append({job_type: employee_profile.objects.get(user=User.objects.get(pk=each.user.pk)).address})
            except:
                pass
        params['job_details']=job_details
        params['application_details']=application_details
        params['worker_details']=worker_details
        params=[params]

        serializer = data_to_real_estate_website_Serializer(data={'input_values': params})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)
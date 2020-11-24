from rest_framework.views import APIView
from job_easy.models import User, job, application,third_party_job_applicants
from rest_framework.response import Response
from .serializers import createdjobSerializer, jobsSerializer, createdApplicationSerializer
from rest_framework import status
import base64
from rest_framework.authtoken.models import Token

# class user_data(APIView):
#
#     def get(self,request):
#         user=User.objects.filter(email=request.query_params.get('email'))[0]
#         serializer = getUserSerializer(user, many=False)
#         return Response(serializer.data)


class post_a_job(APIView):

    def post(self, request):

        try:
            token = request.data['token']
            user = Token.objects.get(key=token).user
            new_job = job(user=user, post_date=request.data['post_date'], last_date=request.data['last_date'],
                          job_title=request.data['job_title'], job_type=request.data['job_type'],
                          job_details_requirements=request.data['job_details_requirements'],
                          job_address=request.data['job_address'], job_salary=request.data['job_salary'],
                          job_other_details=request.data['job_other_details'],
                          job_terms_and_conditions=request.data['job_terms_and_conditions'])

            new_job.save()
            new_employer=third_party_job_applicants(job=new_job,company_name=request.data['company_name'],company_description=request.data['company_description'],company_adress=request.data['company_adress'])
            new_employer.save()
            file = request.data['pro_pic']
            file = base64.b64decode(file)
            filename1 = 'job_easy/media/user_profile_pictures/' + str(new_job.id) + 'job_id' + str(
                new_employer.id) + 'new_employer.jpg'
            with open(filename1, 'wb') as f:
                f.write(file)
            new_employer.user_profile_picture = filename1
            new_employer.save()


            params = [{'job_id': new_job.id}]
            serializer = createdjobSerializer(data={'input_values': params})
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

class job_data(APIView):

    def get(self, request):
        jobs = job.objects.all()
        serializer = jobsSerializer(jobs, many=True)
        return Response(serializer.data)


class post_an_application(APIView):

    def post(self, request):

        try:
            token = request.data['token']
            user = Token.objects.get(key=token).user
            job_id = request.data['job_id']
            job_ = job.objects.get(pk=int(job_id))

            new_application = application(user=user, job=job_, time_stamp=request.data['time_stamp'],
                                          resume_bool=request.data['resume_bool'],
                                          details_and_instructions=request.data['details_and_instructions'],
                                          application_status="yet_to_see")
            new_application.save()
            file = request.data['resume_file_new']
            file = base64.b64decode(file)
            filename1 = 'job_easy/media/resumes/' + job_id + 'job_id' +str(new_application.id)+'application_id.jpg'
            with open(filename1, 'wb') as f:
                f.write(file)
            new_application.resume_file_new=filename1
            new_application.save()

            params = [{'job_id': new_application.id}]
            serializer = createdApplicationSerializer(data={'input_values': params})
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

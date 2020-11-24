from django.shortcuts import render,redirect
from .forms import AddJobPostForm
from job_easy.models import job,employer_profile,application,aadhaar_info
import datetime
from django.contrib import messages
from django.core.files import File
from job_easy.views import verify_aadhaar


def home(request):
    return render(request, 'landing.html')


def add_job_post(request):
    if request.method == "POST":
        form = AddJobPostForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            r=job()

            user=request.user
            r.user=user
            now = datetime.datetime.now()
            x=now.strftime("%d/%m/%Y")
            r.post_date = x
            r.job_title = form.cleaned_data['job_title']
            r.job_address = form.cleaned_data['job_address']
            r.job_type = form.cleaned_data['job_type']
            r.job_salary = form.cleaned_data['job_salary']
            r.job_other_details = form.cleaned_data['job_other_details']
            r.job_details_requirements = form.cleaned_data['job_details_requirements']
            r.last_date = form.cleaned_data['last_date']
            r.job_terms_and_conditions = form.cleaned_data['job_terms_and_conditions']

            r.save()
            if job.objects.filter(user=request.user).exists():
                return redirect('http://127.0.0.1:8000/employer/view_jobs')
            else:
                return redirect('http://127.0.0.1:8000/employer/')
        else:
            messages.error(request,"Invalid Response!!!")
            return render(request, 'Post_job.html')
    else:
        return render(request, 'Post_job.html')


def employer_profile_page(request):
    if request.user.is_employer:

        data = {}
        data['profile_pic'] = employer_profile.objects.get(user=request.user).user_profile_pictures
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['user_name'] = request.user.username
        data['phone_number'] = employer_profile.objects.get(user=request.user).phone_no
        data['email'] = request.user.email
        data['address'] = employer_profile.objects.get(user=request.user).address
        data['verification_status'] = employer_profile.objects.get(user=request.user).verification_status

        data['company_name'] = employer_profile.objects.get(user=request.user).company_name
        data['company_description'] = employer_profile.objects.get(user=request.user).company_description
        data['company_adress'] = employer_profile.objects.get(user=request.user).company_adress

        return render(request, 'profile_view_employer.html', context=data)
    else:
        return render(request, 'landing.html')


def employer_edit_page(request):
    if request.user.is_employer == True:
        if request.method == "POST":

            my_profile = employer_profile.objects.get(user=request.user)

            if request.POST.get('phone_number') != "":
                my_profile.phone_no = request.POST.get('phone_number')
            if request.POST.get("address") != "":
                my_profile.address = request.POST.get("address")
            if request.POST.get("pro_pic") != "":
                f = open(request.POST.get("pro_pic"), 'rb')
                Image = File(f)
                file_name = str(request.user.id) + "user_id" + request.POST.get("pro_pic")
                with open(file_name, 'wb') as new_file:
                    new_file.write(Image.read())
                my_profile.user_profile_pictures = file_name

            if request.POST.get("aadhaar_pic") != "":
                pass
            if request.POST.get("company_name") != "":
                my_profile.company_name = request.POST.get("company_name")
            if request.POST.get("company_address") != "":
                my_profile.company_adress = request.POST.get("company_address")
            if request.POST.get("company_description") != "":
                my_profile.company_description = request.POST.get("company_description")

            my_profile.save()
            return employer_profile_page(request)
        else:
            return render(request, 'profile_edit_employer.html')
    else:
        return render(request, 'landing.html')


def emp_job_listing(request):
    job_posts=job.objects.filter(user=request.user).order_by('post_date')
    return render(request, 'Jobs_posted.html', {'job_posts': job_posts} )


def applicants_page(request):
    jobID = request.POST.get('applicants')
    applications=application.objects.filter(job_id=jobID)
    return render(request, 'View_applications.html', {'applications': applications} )


def job_delete(request):
    JOB_ID = request.POST.get('delete')
    job.objects.get(id=JOB_ID).delete()
    return redirect('http://127.0.0.1:8000/employer/view_jobs')


def update_app_status_to_select(request):
    app_ID = request.POST.get('status')
    k = application.objects.get(id=app_ID)
    k.application_status = "Selected"
    jobID =  k.job.id
    k.save(update_fields=['application_status'])
    applications=application.objects.filter(job_id=jobID)
    return render(request, 'View_applications.html', {'applications': applications} )


def update_app_status_to_reject(request):
    app_ID = request.POST.get('status')
    k = application.objects.get(id=app_ID)
    k.application_status = "Rejected"
    jobID =  k.job.id
    k.save(update_fields=['application_status'])
    applications=application.objects.filter(job_id=jobID)
    return render(request, 'View_applications.html', {'applications': applications} )


def update_app_status_to_delete(request):
    app_ID = request.POST.get('status')
    k = application.objects.get(id=app_ID)
    jobID =  k.job.id
    k.delete()
    applications=application.objects.filter(job_id=jobID)
    return render(request, 'View_applications.html', {'applications': applications} )


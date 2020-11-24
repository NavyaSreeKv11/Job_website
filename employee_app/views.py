from django.shortcuts import render,redirect
from job_easy.models import *
from django.core.files import File
from django.contrib import messages
from job_easy.views import verify_aadhaar
import concurrent.futures
from datetime import datetime
from django.http import HttpResponse


def employee_profile_page(request):
    k = request.GET.get('user_id')
    if employee_profile.objects.filter(user=k):
        k=employee_profile.objects.get(user=k)
        data = {}
        data['profile_pic'] = employee_profile.objects.get(user=k).user_profile_pictures
        data['first_name'] = k.first_name
        data['last_name'] = k.last_name
        data['user_name'] = k.username
        data['phone_number'] = employee_profile.objects.get(user=k).phone_no
        data['email'] = k.email
        data['address'] = employee_profile.objects.get(user=k).address
        data['verification_status'] = employee_profile.objects.get(user=k).verification_status
        data['job_status'] = employee_profile.objects.get(user=k).job_status

        return render(request, 'profile_view_seeker.html', context=data)
    elif request.user.is_employee == True:

        data = {}
        data['profile_pic'] = employee_profile.objects.get(user=request.user).user_profile_pictures
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['user_name'] = request.user.username
        data['phone_number'] = employee_profile.objects.get(user=request.user).phone_no
        data['email'] = request.user.email
        data['address'] = employee_profile.objects.get(user=request.user).address
        data['verification_status'] = employee_profile.objects.get(user=request.user).verification_status
        data['job_status'] = employee_profile.objects.get(user=request.user).job_status

        return render(request, 'profile_view_seeker.html', context=data)
    else:
        messages.error(request, 'You are not an employee.')
        return render(request, 'index.html')


def employee_edit_page(request):
    if request.user.is_employee == True:
        if request.method == "POST":

            my_profile = employee_profile.objects.get(user=request.user)
            user = User.objects.get(username=my_profile.user)
            if request.POST.get('first_name') != "":
                user.first_name= request.POST.get('first_name')
                user.save()
            if request.POST.get("last_name") != "":
                user.last_name = request.POST.get("last_name")
                user.save()
            if request.POST.get('phone_number') != "":
                my_profile.phone_no = request.POST.get('phone_number')
            if request.POST.get("address") != "":
                my_profile.address = request.POST.get("address")
            if request.POST.get("pro_pic") != "":
                f = open(request.POST.get("pro_pic"), 'rb')
                Image=File(f)
                file_name=str(request.user.id)+"user_id"+request.POST.get("pro_pic")
                with open(file_name, 'wb') as new_file:
                    new_file.write(Image.read())
                my_profile.user_profile_pictures = file_name
            if request.POST.get("job_status") != "":
                if request.POST.get("job_status")=="on":
                    my_profile.job_status = True
                else:
                    my_profile.job_status = False
            if request.POST.get("aadhaar_pic") != "":
                pass

            my_profile.save()
            return employee_profile_page(request)
        else:
            return render(request, 'profile_edit_seeker.html')
    else:
        messages.error(request, 'You are not an employee.')
        return render(request, 'index.html')

def View_history_jobs(request):
    data = application.objects.filter(user=request.user)
    data = data.filter(application_status="Selected")
    data_new={}
    for i in data:
        try:
            t = credibility.objects.get(on_user=i.id)
            data_new[i.id]={'name': i, 'comments': t.comments, 'ratings': t.ratings}
        except:
            data_new[i.id]={'name': i}

    return render(request, 'seeker_history.html', {'data_new': data_new})


def View_applied_jobs(request):
    data = application.objects.filter(user=request.user)
    return render(request, 'seeker_applied.html', {'data': data})

def RateJob(request):
    val = request.POST.get('rate')
    comment = request.POST.get('comment')
    user_id = request.POST.get('user_id')
    r = credibility()
    r.user = request.user
    r.ratings = val
    r.comments = comment
    data = application.objects.get(id=user_id)
    r.on_user=data
    r.save()
    return redirect("http://127.0.0.1:8000/employee_history_jobs/")


def saved_jobs(request):
    data = savedjobs.objects.filter(user=request.user)
    return render(request, 'saved_seeker.html', {'data': data})


def view_job(request):
    global job_ID
    job_ID = request.GET.get('job_ID')
    data = job.objects.filter(id=job_ID)
    data_new={}
    for i in data:
        if savedjobs.objects.filter(job_id=job_ID):
            print("HAS")
            data_new[i.id]={'name': i, 'saved': True}
        else:
            data_new[i.id]={'name': i}

    return render(request, 'Job_detail_seeker.html', {'data_new': data_new})


def save_job(request):
    global job_ID
    job_ID = request.GET.get('job_ID')
    t = savedjobs()
    k = job.objects.get(id=job_ID)
    t.job = k
    t.user = request.user
    t.save()
    data = job.objects.filter(id=job_ID)
    data_new = {}
    for i in data:
        if savedjobs.objects.filter(job_id=job_ID):
            print("HAS")
            data_new[i.id]={'name': i, 'saved': True}
        else:
            data_new[i.id]={'name': i}

    return render(request, 'Job_detail_seeker.html', {'data_new': data_new})


def apply_job(request):
    global job_ID
    job_ID = request.GET.get('job_ID')
    data = job.objects.filter(id=job_ID)
    data.job_ID=job_ID
    print(data)
    return render(request, 'Apply_for_job.html', {'data': data})

def job_applied(request):
    if request.method == "POST":
        # print("sfjfkjfk")
        # form = ApplyJobForm(data=request.POST)
        # if form.is_valid():

        r = application()
        user = request.user
        r.user = user
        now = datetime.now()
        r.time_stamp = now
        r.details_and_instructions = request.POST.get('details_and_instructions')
        r.application_status = "Pending"
        r.resume_file_new = request.FILES.get('filename')
        r.job = job.objects.get(pk=int(request.GET.get('job_ID')))
        l = request.GET.get('job_ID')
        g = application.objects.filter(user=request.user)
        g = g.filter(job_id=l)
        if len(g) > 0:
            ######
            return messages.error(request,'already applied')
            return redirect("http://127.0.0.1:8000/employee/View_applied_jobs/")
        r.save()
        if job.objects.filter(user=request.user).exists():
            return redirect("http://127.0.0.1:8000/employee/View_applied_jobs/")
        else:
            return redirect('http://127.0.0.1:8000/search/')
        # else:
        #     return HttpResponse("Invalid Response!!! Go Back to Re-Enter the Form")



from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_data_seeker=models.BooleanField(default=False)

    def __str__(self):
        return self.username


class aadhaar_info(models.Model):
    uid=models.CharField(max_length=20)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    yob=models.CharField(max_length=10)
    co=models.CharField(max_length=150)
    house=models.CharField(max_length=50)
    street=models.CharField(max_length=50)
    loc=models.CharField(max_length=50)
    vtc=models.CharField(max_length=50)
    dist=models.CharField(max_length=50)
    subdist=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pc=models.CharField(max_length=10)



class employee_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    phone_no = models.CharField(max_length=50)
    address = models.TextField(null=True)
    aadhaar_details = models.OneToOneField(aadhaar_info, null=True, blank=True, on_delete=models.CASCADE,
                                           related_name='aadhaar_details_employee')

    user_profile_pictures = models.ImageField(upload_to='user_profile_pictures', blank=True)

    verification_status = models.BooleanField(default=False)
    privacy_status = models.BooleanField(default=False)
    job_status = models.BooleanField(default=False)



class employer_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    phone_no = models.CharField(max_length=50)
    address = models.TextField(null=True)
    aadhaar_details =  models.OneToOneField(aadhaar_info,null=True,blank=True, on_delete=models.CASCADE, related_name='aadhaar_details_employer')
    user_profile_pictures = models.ImageField(upload_to='user_profile_pictures', blank=True)

    company_name=models.CharField(max_length=50)
    company_type = models.CharField(max_length=50)
    company_description=models.TextField(null=True)
    company_adress=models.TextField(null=True)

    verification_status = models.BooleanField(default=False)
    privacy_status = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_employer:
            employer_profile.objects.create(user=instance)
            instance.employer_profile.save()
        elif instance.is_employee:
            employee_profile.objects.create(user=instance)
            instance.employee_profile.save()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_data_seeker:
            Token.objects.create(user=instance)





class job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_user')
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_date = models.DateTimeField(blank=True)

    job_title = models.TextField(null=True)
    job_type = models.CharField(max_length=150)
    job_details_requirements = models.TextField(blank=True)
    job_address = models.TextField(null=True)
    job_salary = models.CharField(max_length=50,blank=True)
    job_other_details = models.TextField(blank=True)
    job_terms_and_conditions = models.TextField(blank=True)


class application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aplication_user')
    job = models.ForeignKey(job, on_delete=models.CASCADE, related_name='job_application')
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)
    resume_bool=models.BooleanField(default=False)
    resume_file_new=models.FileField()
    details_and_instructions=models.TextField(blank=True)
    application_status=models.CharField(max_length=50)


class credibility(models.Model):
    on_user = models.OneToOneField(application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credibility_of_user')
    ratings=models.TextField(null=True)
    comments=models.TextField(null=True)

class savedjobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.OneToOneField(job, on_delete=models.CASCADE)

class third_party_job_applicants(models.Model):
    job = models.ForeignKey(job, on_delete=models.CASCADE, related_name='tpj_user')
    user_profile_picture = models.ImageField(upload_to='user_profile_pictures', blank=True)

    company_name = models.CharField(max_length=50)
    company_description = models.TextField()
    company_adress = models.TextField()

class third_party_application_applicants(models.Model):
    job = models.ForeignKey(job, on_delete=models.CASCADE, related_name='tpa_user')
    user_profile_picture = models.ImageField(upload_to='user_profile_pictures', blank=True)

    phone_no = models.CharField(max_length=50)
    address = models.TextField()
    email=models.EmailField()
    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

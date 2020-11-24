from django.contrib.auth import login as auth_login,logout,authenticate
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes,force_text
from django.core.mail import EmailMessage
import requests
from rest_framework.authtoken.models import Token

from .forms import UserForm
from django.shortcuts import render,redirect
from .models import User
import xml.etree.ElementTree as ET


def index(request):
    return render(request,'index.html')

def user_logout(request):
    logout(request)
    return render(request,'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if user.is_employee==True:
                    return redirect('../search/')
                elif user.is_employer == True:
                    return redirect('http://127.0.0.1:8000/employer/home/')
                else:
                    messages.error(request, 'Thank you for using our API service. But we are sorry to inform that we are not providing window service to API users')
                    logout(request)
                    return render(request, 'login.html')
            else:
                messages.error(request, 'Your account is inactive.')
                return render(request, 'login.html')
        else:
            try:
                if User.objects.get(username=username).is_active==False:
                    messages.error(request, 'Your account is inactive.')
                    return render(request, 'login.html')
            except:
                pass
            messages.error(request, 'username or password is not correct')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')

def signup(request):
    registered=False
    if request.method == 'POST':

        user_form = UserForm(request.POST)

        if user_form.is_valid()and user_form.cleaned_data['password'] == user_form.cleaned_data['confirm_password']:
            employer_status = user_form.cleaned_data['employer_status']

            user = user_form.save(commit=False)
            user.is_active = False
            if employer_status == 'employee':
                user.is_employee = True
            elif employer_status == 'employer':
                user.is_employer = True
            else :
                user.is_data_seeker = True
            user.set_password(user.password)
            user.save()
            registered=True
            current_site = get_current_site(request)
            domain = current_site.domain
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            name = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            response = requests.get(
                "http://api.quickemailverification.com/v1/verify?email=" + to_email + "&apikey=15aef1e3ebf4f0e3357b6aab94bb77833e639fc261b2d32903e1895bd330")
            result = response.json()

            if (result['did_you_mean'] == '' and result['result'] == "valid"):

                mail_subject = 'Activate your blog account.'
                to_email = user_form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                try:
                    email.send()
                except:
                    u = User.objects.get(username=name)
                    u.delete()
                    messages.error(request,'Server problem please register again')
                    return render(request, 'signup.html', {'user_form': user_form})

                return render(request, 'emailsent.html', {})

            else:
                try:
                    u = User.objects.get(username=name)
                    u.delete()
                except User.DoesNotExist:
                    messages.error(request,'The email given is invalid please check it ')
                    return render(request, 'signup.html', {'user_form': user_form})
                except Exception as e:
                    messages.error(request,'The email given is invalid please check it ')
                    return render(request, 'signup.html', {'user_form': user_form})
                messages.error(request,'The email given is invalid please check it ')
                return render(request, 'signup.html', {'user_form': user_form})
        elif user_form.data['password'] != user_form.data['confirm_password']:
            messages.error(request, 'passwords do not match')

    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'user_form': user_form, 'registered': registered})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request,user)
        if user.is_employee == True:
            return redirect('http://127.0.0.1:8000/search/')
        elif user.is_employer == True:
            return redirect('http://127.0.0.1:8000/employer/home/')
        else:

            token_value=Token.objects.get(user=user).key
            messages.error(request,
                           'Thank you for using our API service. But we are sorry to inform that we are not providing window service to API users. Your API key is '+token_value)
            logout(request)
            return render(request, 'http://127.0.0.1:8000/login/')
    else:
        messages.error(request,'Activation link is invalid!')
        return render(request, 'index.html')


def verify_aadhaar(image):
    import cv2
    from aadhar import validate
    print("C:\\Users\sreej.DESKTOP-JSBHQOA\PycharmProjects\\job_easy_final\\"+image)
    inputImage = cv2.imread("C:\\Users\sreej.DESKTOP-JSBHQOA\PycharmProjects\\job_easy_final\\b.jpg")
    qrDecoder = cv2.QRCodeDetector()
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    if len(data) > 0:
        root = ET.fromstring(data)
        data = root.attrib
        if validate(data['uid']):
            return (data, "valid")
        else:
            return ({}, "invalid")
    else:
        return ({},"invalid")


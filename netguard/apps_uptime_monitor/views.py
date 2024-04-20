from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from apps_uptime_monitor.models import userdata, usermapping
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
import uuid, time, pyotp
import requests
import logging

@csrf_exempt
def gen_uid(request):
    otp = pyotp.TOTP('base32secret3232')
    return otp.now()

@csrf_exempt
def login(request):
    #print(timezone.now())
    error_message = None 
    if request.method == 'POST':
        field1_data = request.POST.get('email')   
        field2_data = request.POST.get('password')

        request.session['doctor_email'] = field1_data
        if not userdata.objects.filter(email__iexact=field1_data).exists():
            error_message1 = "Incorrect Email!"
            print("email no exsist")

            messages.success(request, "signup")

            return render(request, "login.html", {'error_message1': error_message1},)
            
        else:  
            user = userdata.objects.get(email=field1_data)
            stored_password = user.password

            if not check_password(field2_data,stored_password):
                error_message1 = "Incorrect password!"
                messages.success(request, "forgot")
                
                return render(request, "login.html", {'error_message1': error_message1},)
            else:
                display_mail = field1_data

                user_temp = userdata.objects.get(email=display_mail)

                log_time = timezone.now()
                print(field1_data)

                new_entry = usermapping(user=user_temp, login_time=log_time)
                temp = usermapping.objects.filter(status=True).values().first()
                print('.............................................................')
                print(temp)
                new_entry.save()

                    
                print(log_time)
                
                request.session['userlog'] = field1_data

                print('.............................................................')

                usertype = user_temp.usertype
                request.session['usertype'] = usertype

                context = {
                    'usertype': usertype,
                    'doctor_email': display_mail
                }

                request.session['context'] = context

                if usertype == "superuser":
                    return redirect('landing')
                else:
                    return redirect('landing')
    else:
        return render(request, "login.html", {'error_message': error_message})
    
@csrf_exempt
def ip_tools(request):
    error_message = None 
    ip_info = None
    if request.method == 'POST':
        ip = request.POST.get('ipaddress')
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        if response.status_code == 200:
            ip_info = response.json()
        else:
            error_message = "IP address lookup failed"
    return render(request, "ipinfo.html", {'error_message': error_message, 'ip_info': ip_info})

@csrf_exempt
def dns_tools(request):
    error_message = None 
    ip_info = None
    if request.method == 'POST':
        domain = request.POST.get('domain')
        url = f"https://networkcalc.com/api/dns/lookup/{domain}"
        response = requests.get(url)
        if response.status_code == 200:
            ip_info = response.json()
        else:
            error_message = "DNS lookup failed"
    return render(request, "dnsinfo.html", {'error_message': error_message, 'ip_info': ip_info})


@csrf_exempt
def certificate_info(request):
    error_message = None 
    certificate_info = None
    if request.method == 'POST':
        domain = request.POST.get('domain')
        url = f"https://networkcalc.com/api/security/certificate/{domain}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                certificate_info = data.get('certificate')
            else:
                error_message = "Certificate information not found"
        else:
            error_message = "Failed to fetch certificate information"
    return render(request, "certificate_info.html", {'error_message': error_message, 'certificate_info': certificate_info})


@csrf_exempt
def subdomain_info(request):
    error_message = None 
    subdomains = None
    if request.method == 'POST':
        domain = request.POST.get('domain')
        url = "https://subdomain-scan1.p.rapidapi.com/"
        querystring = {"domain": domain}
        headers = {
            "X-RapidAPI-Key": settings.API_KEY,
            "X-RapidAPI-Host": "subdomain-scan1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                subdomains = data  # Assuming the response is directly a list of subdomains
            elif isinstance(data, dict) and data.get('status') == 'OK':
                subdomains = data.get('subdomains')  # Access the subdomains from the dictionary
            else:
                error_message = "Subdomain information not found"
        else:
            error_message = "Failed to fetch subdomain information"
    return render(request, "subdomain_info.html", {'error_message': error_message, 'subdomains': subdomains})

@csrf_exempt
def security_tools(request):
    return render(request, 'security-tools.html')


@csrf_exempt
def landing(request):
    return render(request, 'superuser-landing.html')

@csrf_exempt
def signup(request):
    error_message = ""
    if request.method == 'POST':

        u_id = gen_uid(request)

        field1_data = request.POST.get('username')
        field2_data = request.POST.get('email')
        field3_data = request.POST.get('password')

        if userdata.objects.filter(email=field2_data).exists():

            error_message = "Email already exists in the database."
            messages.success(request, "login")
            return render(request, "signup.html", {'error_message': error_message},)

        else:
            request.session['username'] = field1_data
            request.session['email'] = field2_data
            request.session['password'] = field3_data
            request.session['otp'] = u_id



            subject = 'Welcome to Aerobiosys'
            message = f'Hi {field1_data}, thank you for signing up with Aerobiosys. This is your One Time Password : {u_id}'
            email_from = settings.EMAIL_HOST_USER
            print(field2_data)
            recipient_list = [field2_data]
            send_mail( subject, message, email_from, recipient_list )

            return redirect('otp')



    else:
        return render(request, "signup.html", {'error_message': error_message})

@csrf_exempt
def otp(request):
    user_email = request.session.get('email')
    user_name = request.session.get('username')
    user_password = request.session.get('password')
    user_otp = request.session.get('otp')
    error_message = None

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        if user_email:
            try:

                if entered_otp == user_otp:
                    hashed_password = make_password(user_password)
                    new_entry = userdata(username=user_name, email=user_email, password=hashed_password, usertype="user")
                    new_entry.save()
                    return redirect('login')

                else:
                    messages.success(request, "Incorrect OTP")
                    return render(request,"otp.html")

            except userdata.DoesNotExist:
                error_message = "User not found or email not available."
        else:
            error_message = "User email not available in session."

    else:
        return render(request, "otp.html", {'error_message': error_message})
    
@csrf_exempt
def logout(request):

    log_user = request.session.get('userlog')
    log_device = request.session.get('devicelog')

    user_temp = userdata.objects.get(email=log_user)
    device_temp = devicedata.objects.get(serial_number=log_device)

    temp = usermapping.objects.filter(user=user_temp, device=device_temp, status=True).first()
    temp = usermapping.objects.filter(status=True).first()
    print(temp)
    if temp:

        temp.logout_time = timezone.now()
        temp.status = False
        temp.save()

    if temp:
        temp.logout_time = timezone.now()
        print(temp)
    return redirect('login')

@csrf_exempt
def forgot_otp(request):
    user_email = request.session.get('email')
    user_otp = request.session.get('otp')
    error_message = None
    print(user_otp)
    if request.method == 'POST':

        new_password = request.POST.get('password')
        entered_otp = request.POST.get('otp')
        if user_email:
            try:

                if entered_otp == user_otp:
                    print("checksuccess1")
                    hashed_password = make_password(new_password)
                    t = userdata.objects.get(email=user_email)
                    t.password = hashed_password
                    t.save()
                    print("checksuccess2")
                    return redirect("login")

                else:
                    messages.success(request, "Incorrect OTP")
                    return render(request,"forgototp.html")

            except userdata.DoesNotExist:
                error_message = "User not found or email not available."
        else:
            error_message = "User email not available in session."
    else:
        return render(request, "forgototp.html", {'error_message': error_message})

@csrf_exempt
def forgot(request):
    error_message = None
    if request.method == 'POST':
        field1_data = request.POST.get('email')

        if not userdata.objects.filter(email__iexact=field1_data).exists():
            error_message1 = "Incorrect Email!"
            print("email no exsist")

            messages.success(request, "signup")

            return render(request, "forgot.html", {'error_message1': error_message1})

        else:
            u_id = gen_uid(request)

            subject = 'Security Alert'
            message = f'Hi {field1_data}.This is your One Time Password : {u_id}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [field1_data]
            send_mail( subject, message, email_from, recipient_list )

            request.session['otp'] = u_id
            request.session['email'] = field1_data
            return redirect('forgot_otp')

    else:
        return render(request, "forgot.html", {'error_message': error_message})
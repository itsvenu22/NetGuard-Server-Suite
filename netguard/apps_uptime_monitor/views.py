from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import userdata
from aerodevice.models import usermapping, devicedata
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.mail import send_mail
import uuid, time, pyotp
from django.contrib import messages
from django.utils import timezone

@csrf_exempt
def gen_uid():
    otp = pyotp.TOTP('base32secret3232')
    return otp.now()
@csrf_exempt
def signup(request):
    error_message = None 
    if request.method == 'POST':
        
        u_id = gen_uid()

        field1_data = request.POST.get('username')  
        field2_data = request.POST.get('email')   
        field3_data = request.POST.get('password')

        if userdata.objects.filter(email=field2_data).exists():
        
            error_message = "Email already exists in the database."
            return render(request, "signup.html", {'error_message': error_message})
        
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
                    new_entry = userdata(username=user_name, email=user_email, password=hashed_password)
                    new_entry.save()
                    login(request)
                
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
def login(request):
    #print(timezone.now())
    error_message = None 
    if request.method == 'POST':
        field1_data = request.POST.get('email')   
        field2_data = request.POST.get('password')
        field3_data = request.POST.get('sno')

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
                try: 
                    device_temp = devicedata.objects.get(serial_number=field3_data)
                except Exception as e:
                    error_message1 = "Incorrect Serial Number!"
                    messages.success(request, "forgot")
                    
                    return render(request, "login.html", {'error_message1': error_message1},)
                log_time = timezone.now()
                print(field1_data)

                new_entry = usermapping(user=user_temp, device=device_temp, login_time=log_time)
                temp = usermapping.objects.filter(status=True).values().first()
                print('.............................................................')
                print(temp)
                new_entry.save()

                    
                print(log_time)
                
                request.session['userlog'] = field1_data
                request.session['devicelog'] = field3_data

                print('.............................................................')

                usertype = user_temp.usertype
                request.session['usertype'] = usertype

                context = {
                    'usertype': usertype,
                    'doctor_email': display_mail
                }

                request.session['context'] = context

                if usertype == "Superuser":
                    return render(request,"superlanding.html", context,)
                else:
                    return render(request,"landing.html", context,)
    else:
        return render(request, "login.html", {'error_message': error_message})
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
            u_id = gen_uid()

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
    
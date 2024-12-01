from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from products.models import Product,Variant
import random
from datetime import datetime,timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from.validators import validate_first_name,validate_last_name,validate_email,validate_password,validate_username,validate_phone


# Create your views here.

User= get_user_model()

#======================Function to send otp,email=====================# 

def generateOtp():   
    return str(random.randint(1000,9999))


def send_email_otp(email,otp):
    try:
        subject='OTP Verification'
        message=f'Your OTP for register soundwave is :{otp}'
        sender=settings.EMAIL_HOST_USER 
        receiver=[email]
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False
        )
        return True
    except BadHeaderError:
        print('BadHeaderError: Invalid header found in email.')
    except Exception as e:
        print(f'Error sending OTP via email:{e}')

#======================Function to send otp and email End=====================# 


#======================Signup session=====================# 
@never_cache
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')

        error_message = {}
        error_message['firstname_error'] = validate_first_name(first_name)
        error_message['last_name_error'] = validate_last_name(last_name)

        if User.objects.filter(username=username).exists():
            error_message['username_error'] = 'Username already exists'
        else:
            error_message['username_error'] = validate_username(username)
        if User.objects.filter(email=email).exists():
            error_message['email_error'] = 'Email already exists'
        else:
            error_message['email_error'] = validate_email(email)
        if User.objects.filter(phone_number=phone_number).exists():
            error_message['phone_number_error'] = 'Phone number already exists'
        else:
            error_message['phone_number_error'] = validate_phone(phone_number)
        if password != confirm_password:
            error_message['password_error'] = 'Passwords do not match'
        else:
            error_message['password_error'] = validate_password(password)

        if any(error_message.values()):
            return render(request, 'user/signup.html', {'error_message': error_message, 'input_data': request.POST})

        otp = generateOtp()
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['username'] = username
        request.session['email'] = email
        request.session['phone_number'] = phone_number
        request.session['password'] = password
        request.session['otp_value'] = otp
        request.session['otp_expiration'] = (timezone.now() + timedelta(minutes=5)).isoformat()

        if send_email_otp(email, otp):
            messages.success(request, 'OTP has been sent to your email!')
            return redirect('otp_validation')
        else:
            messages.error(request, 'Failed to send OTP. Please try again.')
            return render(request, 'user/signup.html', {'error_message': error_message, 'input_data': request.POST})
    return render(request, 'user/signup.html')

#======================Signup session End=====================# 


#======================OTP validation session=====================# 
@never_cache
def otp_generation(request):
    if request.method=='POST':
        first_name=request.session.get('first_name')
        last_name=request.session.get('last_name')
        username=request.session.get('username')
        email=request.session.get('email')
        phone_number=request.session.get('phone_number')
        password=request.session.get('password')
        otp_stored=request.session.get('otp_value')
        otp_expiration_str=request.session.get('otp_expiration')
       
        if not otp_expiration_str or not isinstance(otp_expiration_str,str):
            messages.error(request,'otp expiration data is invalid ')
            return redirect('otp_validation')

        try:
            otp_expiration=datetime.fromisoformat(otp_expiration_str)
        except ValueError:
            messages.error(request,'otp expiration format is invalid')
            return redirect('otp_validation')

        otp_enterd=request.POST.get('otp')
        
        if otp_stored==otp_enterd:

            if now()<otp_expiration:
                user=User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number
                )
                user.set_password(password)
                user.save()
                request.session.flush()
                messages.success(request,'account created successfuly')
                return redirect('user_login')
            else:
                messages.error(request,'otp has expired')
                return redirect('otp_validation')
        else:
            messages.error(request,'invalid OTP')
            return redirect('otp_validation')
    return render(request,'user/otp_validation.html')


@never_cache
def resend_otp(request):
    email=request.session.get('email')
    if not email:
        return redirect('signup')
    new_otp=generateOtp()
    request.session['otp_value']=new_otp
    otp_expiraion=timezone.now() + timezone.timedelta(minutes=3)
    request.session['otp_expiration'] = otp_expiraion.isoformat()

    send_email_otp(email,new_otp)
    messages.success(request,'A new OTP is has been send to your email')
    return redirect('otp_validation')

#======================OTP validation session End=====================# 


#====================== User Login,Logout=====================# 
@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username_or_email = request.POST.get('username_or_email')
        password_check= request.POST.get('password')
        user = None
        try:
            user_by_email=User.objects.get(email=username_or_email)
            user=authenticate(request,username=user_by_email,password=password_check)
        except User.DoesNotExist:
            user=authenticate(request,username=username_or_email,password=password_check)
        
        if user is not None and user is not False:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials')

    return render(request,'user/login.html')
    
@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        request.session.flush()
        logout(request)
        return redirect('user_login')
    return redirect('home')
 
#======================User Login,Logout End=====================# 


#======================Homepage session=====================# 
@never_cache
def homepage(request):
    featured_products = Product.objects.filter(is_listed=True).prefetch_related('variants').order_by('-created_at')
    new_arrivals=Product.objects.prefetch_related('variants').order_by('created_at')
    return render(request, 'user/index.html', {'featured_products': featured_products,'new_arrivals':new_arrivals})

#======================Homepage session End=====================# 


#======================Products_page session=====================# 
@never_cache
@login_required
def product_page(request):
    products=Product.objects.filter(is_listed=True).prefetch_related('variants').all()
    return render(request,'user/product_list.html',{'products':products})

#======================Product_page session End=====================# 


#======================Product_details session=====================# 
@never_cache
@login_required
def details_pro(request,product_id,variant_id):
    product=get_object_or_404(Product,id=product_id,is_listed=True)
    variants=get_object_or_404(Variant,id=variant_id,product=product)
    return render(request,'user/product_info.html',{'variants':variants,'product':product})

#======================Product_details session End=====================# 

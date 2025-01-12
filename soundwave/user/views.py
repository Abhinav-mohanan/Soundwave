from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from products.models import Product,Variant,Category,Brand
import random
from datetime import datetime,timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from.validators import validate_first_name,validate_last_name,validate_email,validate_password,validate_username,validate_phone
from offer.models import Brand_offer,Product_offer
from django.db.models import Sum,Count,Q
from django.db.models import Prefetch

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
        pass
    except Exception as e:
        pass

#======================Function to send otp and email End=====================# 


#======================Signup section=====================# 
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

#======================Signup section End=====================# 


#======================OTP validation section=====================# 
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

#======================OTP validation section End=====================# 


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
 
#==================User Login,Logout End===================# 


#======================Forgot_password=====================# 
@never_cache
def forgotpassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
            otp=generateOtp()
            request.session['otp'] = otp
            request.session['email'] = email

            subject='Your OTP for soundwave password reset'
            message=f'Hello, /n Your OTP for resetting soundwave password is {otp} '
            sender=settings.EMAIL_HOST_USER 
            receiver=[email]
            try:
                send_mail(subject,message,sender,receiver)
                return redirect('forgot_password_verify')
            except Exception:
                error_message='Error sending OTP please try again later'
                return render(request,'user/forgot_password.html',{'error_message':error_message})
        else:
            error_message='The email not registered please Signup'
            return render(request,'user/forgot_password.html',{'error_message':error_message})
    return render(request,'user/forgot_password.html')


def forgot_password_verify(request):
    error_message=None
    if request.method=='POST':
        otp=request.POST.get('otp')
        session_otp=request.session.get('otp')
        if otp==session_otp:
            del request.session['otp']
            return redirect('reset_password')
        else:
            error_message='Invalid otp Please try again'
            return render(request,'user/forgot_password_verify.html',{'error_message':error_message})
    return render(request,'user/forgot_password_verify.html')



def reset_password(request):
    error_message=None
    email=request.session.get('email')
    if not email:
        return redirect('forgot_password')
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        error_message='User not found!'
        return render(request,'user/forgot_password_reset.html',{'error_message':error_message})

    if request.method=='POST':
        new_password=request.POST.get('new-password')
        confirm_password=request.POST.get('confirm-password')
        if new_password!=confirm_password:
            error_message='Passwords donot match '
        else:
            error_message=validate_password(new_password)
        if error_message:
            return render(request,'user/forgot_password_reset.html',{'error_message':error_message})
        
        user.set_password(new_password)
        user.save()

        if 'email' in request.session:
            del request.session['email']
        return redirect('user_login')
    return render(request,'user/forgot_password_reset.html')


#======================Forgot_password End=====================# 




#======================Homepage section=====================# 
@never_cache
def homepage(request):
    listed_variants=Variant.objects.filter(is_listed=True,stock__gt=0)
    categories=Category.objects.filter(is_listed=True)
    hero_product=Product.objects.filter(is_listed=True,brand__is_listed=True,category__is_listed=True).prefetch_related(Prefetch('variants',queryset=listed_variants)).order_by('-created_at').first()
    featured_products = Product.objects.filter(is_listed=True,brand__is_listed=True,category__is_listed=True).prefetch_related(Prefetch('variants', queryset=listed_variants)).order_by('-created_at')[:4]
    new_arrivals=Product.objects.filter(is_listed=True,brand__is_listed=True,category__is_listed=True).prefetch_related(Prefetch('variants',queryset=listed_variants)).order_by('name','-created_at')[:5]    

    return render(request, 'user/index.html', {'featured_products': featured_products,'new_arrivals':new_arrivals,
                                               'categories':categories,'hero_product':hero_product})

#======================Homepage section End=====================# 


#======================Products_page session=====================# 
@never_cache
def product_page(request):

    listed_variants = Variant.objects.filter(is_listed=True, stock__gt=0)
    products = Product.objects.filter(
        is_listed=True,
        brand__is_listed=True,
        category__is_listed=True
    ).prefetch_related(Prefetch('variants', queryset=listed_variants))

    filter_applied=False

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    search_query= request.GET.get('query')
    if search_query:
        products=products.filter(name__icontains=search_query)

    price_filter = request.GET.get('price') 
    if price_filter:
        if price_filter == "under_50000":
            products = products.filter(price__gte=30000,price__lte=50000)
        elif price_filter == "10000_30000":
            products = products.filter(price__gte=10000, price__lte=30000)
        elif price_filter == "above_50000":
            products = products.filter(price__gt=50000)
        filter_applied=True

    color_filter = request.GET.get('color')
    if color_filter:
        products = products.filter(variants__color__iexact=color_filter, variants__stock__gt=0)
        filter_applied=True

    sort_filter=request.GET.get('sort')
    if sort_filter =='asc':
        products=products.order_by('name')
        filter_applied=True
       
    elif sort_filter=='desc':
        products=products.order_by('-name')
        filter_applied=True
    
    products = products.distinct()
    selected_category = Category.objects.filter(id=category_id).first() if category_id else None

    return render(request, 'user/product_list.html', {'products': products,'selected_category': selected_category,'search_query':search_query,'filter_applied':filter_applied})



#======================Product_page session End=====================# 


#======================Product_details session=====================# 
@never_cache
def product_detail(request,product_id,variant_id):
    product=get_object_or_404(Product,id=product_id)
    try:
        variants = Variant.objects.get(id=variant_id,product=product)
    except Variant.DoesNotExist:
        variants = None
    all_variant=Variant.objects.filter(product=product)
    images = [variants.image1, variants.image2, variants.image3]

    
    current_date =now().date()
    
    product_offer =Product_offer.objects.filter(
        product=product,
        started_date__lte=current_date,
        end_date__gte=current_date,
        status=True
    ).first()

    brand_offer=Brand_offer.objects.filter(
        brand=product.brand,
        started_date__lte=current_date,
        end_date__gte=current_date,
        status=True
    ).first()
    product_discount_price=None
    brand_discount_price=None

    if product_offer:
        product_discount_price=round(product.price * (1-(product_offer.offer_percentage/100)),0)
    
    if brand_offer:
        brand_discount_price =round(product.price * (1- (brand_offer.offer_percentage/100)),0)

    if product_discount_price is not None and brand_discount_price is not None:
        final_discount_price=float(min(product_discount_price,brand_discount_price))
        active_offer = product_offer if product_discount_price < brand_discount_price else brand_offer 
    elif product_discount_price is not None:
        final_discount_price=float(product_discount_price)
        active_offer=product_offer
    elif brand_discount_price is not None:
        final_discount_price = float(brand_discount_price)
        active_offer = brand_offer
    else:
        final_discount_price=product.price
        active_offer =None

    return render(request,'user/product_info.html',{'variants':variants,'product':product,
                                                    'all_variant':all_variant,'final_discount_price':final_discount_price,
                                                    'active_offer':active_offer,'images':images})

#======================Product_details session End=====================# 


#====================== Product_Search=====================# 
def search_view(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)  
    return render(request, 'user/products.html',{'products': products,'search_query': query})

#====================== Product_Search End=====================# 


#=======================About us =====================# 
def about_us(request):
    total_brands=Brand.objects.aggregate(total=Count('id'))['total']
    total_users=User.objects.exclude(is_superuser=True).aggregate(total_users=Count('id'))['total_users']
    total_products=Variant.objects.aggregate(total_products=Count('id'))['total_products']
    return render(request,'user/about_us.html',{'total_brands':total_brands,'total_users':total_users,'total_products':total_products})

#=======================About us =====================# 


#=======================Help page =====================# 
def helppage(request):
    return render(request,'user/help.html')
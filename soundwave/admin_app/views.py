from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
from django.contrib.auth.models import User
from user.models import CustomUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from products.models import Category,Brand,Product,Variant
from django.contrib.auth import get_user_model



# Create your views here.

User=get_user_model()

#======================Admin login,logout=====================# 
@never_cache
def admin_login(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request,'You are not authorized user')
        else:
            messages.error(request,'invalid username or password!')
    return render(request,'admin/adminlogin.html')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def admin_logout(request):
    if request.method=='POST':
        logout(request)
    return redirect('admin_login')

#======================Admin login,logout End=====================# 



#======================Dashboard session=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def admin_home(request):
    return render(request,'admin/homepage.html')


#======================User managment session=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def user_managment(request):
    user_info=CustomUser.objects.filter(is_staff=False)
    return render(request,'admin/userview.html',{'user_info':user_info})


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def block_user(request,id):
    user=get_object_or_404(User,id=id)
    user.is_active=False
    user.save()
    return redirect('list_user')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def unblock_user(requset,id):
    user=get_object_or_404(User,id=id)
    user.is_active=True
    user.save()
    return redirect('list_user')

#======================User managment session End=====================# 


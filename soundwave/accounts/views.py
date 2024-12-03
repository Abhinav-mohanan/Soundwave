from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .form import Addressform
from django.contrib import messages
from .models import Address

from django.views.decorators.cache import never_cache

# Create your views here.


#=========================USER ACCOUNT VIEW==============================#
@login_required
def user_account_view(request):
    user=request.user
    context={
        'name':user.first_name +' '+ user.last_name,
        'email': user.email,
        'first_name':user.first_name,
        'last_name': user.last_name,
        'phone_number':user.phone_number,
    }
    return render(request,'user/user_account.html',context)

#=========================USER ACCOUNT VIEW End==============================#


#=========================USER ADDRESS VIEW,EDIT==============================#
@never_cache
@login_required
def add_address(request):
    if request.method=='POST':
        form =Addressform(request.POST)
        if form.is_valid():
            address =form.save(commit=False)
            address.user=request.user
            address.save()
            messages.success(request,'your address has been added successfully')
            return redirect('view_address')
        else:
            messages.error(request,'Please correct the form and try again.')
    else:
        form=Addressform()

    return render(request,'user/add_address.html',{'form':form})  

@never_cache
@login_required
def view_address(request):
    addresses=Address.objects.filter(user=request.user)
    return render(request,'user/address.html',{'addresses':addresses})

#=========================USER ADDRESS VIEW,EDIT End==============================#


#=========================USER ORDER VIEW==============================#
@never_cache
@login_required
def view_orders(request):
    return render(request,'user/order_details.html')
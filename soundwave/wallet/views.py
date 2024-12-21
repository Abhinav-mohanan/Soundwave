from django.shortcuts import render

# Create your views here.
def wallet_view(request):
    return render(request,'user/wallet.html')
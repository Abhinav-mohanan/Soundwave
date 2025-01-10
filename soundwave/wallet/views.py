from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . models import Wallet,Transaction
from django.contrib import messages
# Create your views here.

@never_cache
@login_required
def wallet_view(request):
    user=request.user
    try:
        user_wallet=Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        user_wallet=None

    
    if not user_wallet:
        return render(request,'user/wallet.html',{'user_wallet':None})
    
    credit_transactions=Transaction.objects.filter(wallet=user_wallet,transaction_type='Credit').order_by('-created_at')
    debt_transactions=Transaction.objects.filter(wallet=user_wallet,transaction_type='Debit').order_by('-created_at')
        
    return render(request,'user/wallet.html',{'wallet_balance':user_wallet.balance,'credit_transactions':credit_transactions,'debit_transactions':debt_transactions})
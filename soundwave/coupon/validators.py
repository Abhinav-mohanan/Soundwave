from decimal import Decimal
from django.utils.dateparse import parse_date
from .models import Coupon

def validate_coupon(data, coupon=None):
    errors = []

    code = data.get('code')
    if not code:
        errors.append('Coupon code is required.')
    elif len(code) < 4:
        errors.append('Coupon code must be at least 4 characters long.')
    else:
        if coupon:
            if Coupon.objects.filter(code__iexact=code).exclude(coupon_id=coupon.coupon_id).exists():
                errors.append('This coupon code already exists.')
        else:
            if Coupon.objects.filter(code__iexact=code).exists():
                errors.append('This coupon code already exists.')

    coupon_type = data.get('coupon_type')
    if coupon_type not in ['fixed', 'percentage']:
        errors.append('Invalid coupon type. Must be "fixed" or "percentage".')

    try:
        discount_amount = Decimal(data.get('discount_amount', 0))
        if discount_amount <= 0:
            errors.append('The discount amount must be greater than 0.')
        elif coupon_type == 'fixed' and discount_amount > 500:
            errors.append('Fixed discount must not exceed 500.')
        elif coupon_type == 'percentage' and discount_amount > 100:
            errors.append('Percentage discount must not exceed 100%.')
    except (ValueError, TypeError):
        errors.append('Discount amount must be a valid number.')

    try:
        min_purchase_amount = Decimal(data.get('min_purchase_amount', 0))
        if min_purchase_amount <= 0:
            errors.append('Minimum purchase amount must be greater than 0.')
    except (ValueError, TypeError):
        errors.append('Minimum purchase amount must be a valid number.')

    valid_from = data.get('valid_from')
    valid_to = data.get('valid_to')
    if not valid_from or not valid_to:
        errors.append('Both "valid from" and "valid to" dates are required.')
    else:
        valid_from = parse_date(valid_from)
        valid_to = parse_date(valid_to)
        if not valid_from or not valid_to:
            errors.append('Invalid date format.')
        elif valid_from > valid_to:
            errors.append('"Valid from" date must be earlier than "valid to" date.')

    try:
        usage_limit = int(data.get('usage_limit', 0))
        if usage_limit <= 0:
            errors.append('Usage limit must be greater than 0.')
    except (ValueError, TypeError):
        errors.append('Usage limit must be a valid integer.')

    return errors




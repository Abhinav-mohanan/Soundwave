from django.utils import timezone
from offer.models import Product_offer, Brand_offer

def get_address_snapshot(address):
    return {
        'shipping_name': address.name,
        'shipping_address_title': address.address_title,
        'shipping_state': address.state,
        'shipping_city': address.city,
        'shipping_pin': address.pin,
        'shipping_landmark': address.landmark,
        'shipping_phone_number': address.phone_number,
    }


def calculate_total_amount(cart_items):
    total = 0

    for cart_item in cart_items:
        variant = cart_item.variant
        product = variant.product

        current_date = timezone.now().date()

        product_offer = Product_offer.objects.filter(
            product=product,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        brand_offer = Brand_offer.objects.filter(
            brand=product.brand,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        product_price = product.price

        if product_offer:
            product_offer_price = (
                product.price * (1 - product_offer.offer_percentage /100)
            )
        else:
            product_offer_price = None

        if brand_offer:
            brand_offer_price = (
                product.price * (1 - brand_offer.offer_percentage /100)
            )
        else:
            brand_offer_price = None

        if product_offer_price is not None and brand_offer_price is not None:
            final_price =max(
                product_offer_price, brand_offer_price
            )
        elif product_offer_price is not None:
            final_price = product_offer_price
        elif brand_offer_price is not None:
            final_price = brand_offer_price
        else:
            final_price = product.price

        total += final_price * cart_item.quantity

        return round(total, 2)
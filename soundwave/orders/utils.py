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
import re
from django.contrib.auth import get_user_model

User=get_user_model()

def phone_validate(phone, user_id=None):
    pattern = r'^[9876]\d{9}$'
    if not re.match(pattern, phone):
        return 'Enter a valid phone number.'
    if not phone.strip():
        return 'Phone number cannot be blank.'

    if User.objects.exclude(id=user_id).filter(phone_number=phone).exists():
        return 'Phone number already exists.'
    return None

def validate_password(password):

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,30}$'
    if not re.match(pattern, password):
        return 'Password must be 6-30 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.'
    if not password.strip():
        return 'Password cannot be empty'
    return ''

import re

def validate_first_name(first_name):
    pattern = r"^[a-zA-Z-' ]{2,30}$"
    print(f"Validating first_name: {first_name}")
    if not re.match(pattern, first_name):
        print("First name did not match pattern!")
        return 'Enter a valid First name.'
    if not first_name.strip():
        return 'First name cannot be blank.'
    return None

def validate_last_name(last_name):
    pattern = r"^[a-zA-Z-' ]+$"
    print(f"Validating last_name: {last_name}")
    if not re.match(pattern, last_name):
        print("Last name did not match pattern!")
        return 'Enter a valid Last name.'
    if last_name.startswith(' '):
        return 'Last name cannot start with a space.'
    if not last_name.strip():
        return 'Last name cannot be blank.'
    return None


def validate_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern,email):
        return 'Enter a valid Email'
    if not email.strip():
        return 'Email cannot be blank'
    if email != email.strip():
        return 'Email should not contain unwanted spaces'
    return ''
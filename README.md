# 🎧 Soundwave

A full-stack E-commerce Application for audio products such as headphones, speakers, soundbars, and earbuds. Built using Django with a server-rendered architecture, 
Soundwave provides a seamless shopping experience with secure authentication, advanced product management, and a complete order processing system.

## Features

### Authentication & Security
* **OTP-Based Authentication:** Secure signup and password reset using email OTP verification.
* **Multiple Login Options:** Users can log in using username or email.
* **Google Authentication:** Integrated social login using Django Allauth.
* **Secure Session Handling:** Ensures safe user authentication and session management.

### User Experience
* **Product Catalog:** Browse products with categories, brands, and variants.
* **Advanced Filtering:** Filter products by category, price range, color, and sorting options.
* **Cart & Wishlist:** Add, remove, and manage items easily.
* **Checkout System:** Smooth checkout experience with multiple payment options.
* **Order Management:** Track orders, cancel items, request returns, and download invoices.
* **Wallet System:** Manage wallet balance and view transaction history.

### Offers & Discounts
* **Product & Brand Offers:** Time-based promotional discounts.
* **Coupon System:** Apply fixed or percentage-based coupons during checkout.

### Payment System
* **Multiple Payment Options:**
  - Cash on Delivery (COD)
  - Razorpay (Online Payment)
  - Wallet Payment
* **Retry Failed Payments:** Seamless retry mechanism for failed transactions.
* **Refund Handling:** Wallet-based refund processing.

### Admin Dashboard
* **Product Management:** Add, edit, and manage products, categories, brands, and variants.
* **User Management:** Monitor and manage registered users.
* **Order Management:** View and update order statuses.
* **Offer & Coupon Management:** Create and control discounts.
* **Sales Analytics:** Visual insights into revenue and top-selling products.
* **Report Generation:** Export sales reports in PDF and Excel formats.

## Tech Stack


| Component | Technology |
| :--- | :--- |
| **Backend** | Python & Django |
| **Database** | PostgreSQL |
| **Frontend** | HTML/Django Templates |
| **Reports** | ReportLab, OpenPyXL |


## 🔧 Installation & Setup

### Prerequisites
- Python and pip
- PostgreSQL database

```bash
# Clone the Repository
git clone https://github.com/Abhinav-mohanan/Soundwave.git
cd soundwave

# Create Virtual Environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Install Dependencies
pip install -r requirements.txt

# Configure Environment Variables
Create a `.env` file in the Backend/ directory (see Environment Variables below)

# Apply Migrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

# Run Development Server
python manage.py runserver

```

## Environment Variables

```bash
# Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
NAME=your_db_name
USER=your_db_user
PASSWORD=your_db_password
HOST=127.0.0.1
PORT=5432

# Email (OTP)
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

# Google Auth
client_id=your_google_client_id
secret=your_google_secret

# Razorpay
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

## 👨‍💻 Author
Abhinav Mohanan  
*Software Engineer*  

📧 Email: abhinavmohanan018@gmail.com  

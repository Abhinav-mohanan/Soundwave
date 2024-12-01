from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from products.models import Category,Brand,Product,Variant
from django.contrib.auth import get_user_model


# Create your views here.

User=get_user_model

#======================category session=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_category(request):
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        if name:
            Category.objects.create(name=name,description=description)
            messages.success(request,'category added successfully!.')
            return redirect('list_category')
        else:
            messages.error(request,'category name is required! ')  
    return render(request,'admin/add_category.html')


@never_cache
@user_passes_test(lambda u: u.is_superuser,login_url='/adminn/')
def edit_category(request,id):
    category=get_object_or_404(Category,id=id)
    if request.method=='POST': 
        name=request.POST['name']
        description=request.POST['description']
        category_exists=Category.objects.filter(name__iexact=name).exclude(id=category.id).exists()
        if category_exists:
            messages.error(request,f'category{name} already exists')
        else:
            category.name=name
            category.description=description
            category.save()
            messages.success(request,'Category updated successfully')
            return redirect('list_category')
    return render(request,'admin/edit_category.html',{'category':category})


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def view_category(request):
    categories=Category.objects.all()
    return render(request,'admin/category.html',{'categories':categories})


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def list_category(request,id):
    category=get_object_or_404(Category, id=id)
    category.is_listed=True
    category.save()
    return redirect('list_category')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')   
def unlist_category(request,id):
    category=get_object_or_404(Category, id=id)
    category.is_listed=False
    category.save()
    return redirect('list_category')

#======================Dashboard session End=====================# 


#======================Brand session=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_brand(request):
    if request.method=='POST':
        name=request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            messages.success(request,'Brand added successfully!')
            return redirect('list_brand')
        else:
            messages.error(request,"Brand name is required")
    return render(request,'admin/add_brands.html')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def edit_brand(request,id):
    brand=get_object_or_404(Brand,id=id)
    if request.method=='POST':
        name=request.POST['name']
        brand_exists=Brand.objects.filter(name__iexact=name).exclude(id=brand.id).exists()
        if brand_exists:
            messages.error(request,f'Brand {name} is already exists')
        else:
            brand.name=name
            brand.save()
            messages.success(request,'Brand updated sucessfully')
            return redirect('list_brand')        
    return render(request,'admin/edit_brands.html',{'brand':brand})


@never_cache
@user_passes_test(lambda u:u.is_superuser,login_url='/adminn/')
def view_brand(request):
    brands=Brand.objects.all()
    return render(request,'admin/brand.html',{'brands':brands})


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def list_brand(request,id):
    brand=get_object_or_404(Brand, id=id)
    brand.is_listed=True
    brand.save()
    return redirect('list_brand')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')   
def unlist_brand(request,id):
    brand=get_object_or_404(Brand, id=id)
    brand.is_listed=False
    brand.save()
    return redirect('list_brand')

#======================Brand session End=====================# 


#======================Product session=====================# 
@login_required
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_products(request):
    categories=Category.objects.all()
    brands=Brand.objects.all()
    if request.method=='POST':
        name=request.POST.get('name')
        category=request.POST.get('category')
        brand=request.POST.get('brand')
        features=request.POST.get('features')
        price=request.POST.get('price')
        description=request.POST.get('description')
        if all(field.strip() for field in [name, price, description, category, brand, features]):
            if not name:
                 messages.error(request, "Product name is required.")
            elif not category:
                messages.error(request, "Category is required.")
            elif not brand:
                messages.error(request, "Brand is required.")
            elif not features:
                messages.error(request, "Features are required.")
            elif not price:
                messages.error(request, "Price is required.")
            elif not description:
                messages.error(request, "Description is required.")
            else:
                category = get_object_or_404(Category, id=category)
                brand = get_object_or_404(Brand, id=brand)
                Product.objects.create(
                name=name,
                description=description,
                category=category,
                feature=features,
                brand=brand,
                price=price,
                )
                messages.success(request, "Product added successfully.")
                return redirect('list_product')       
    return render(request,'admin/addproducts.html',{'brands':brands,'categories':categories})


@never_cache
@login_required
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def view_product(request):
    products=Product.objects.all()
    return render(request,'admin/products.html',{'products':products})


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def list_product(request,id):
    product=get_object_or_404(Product, id=id)
    product.is_listed=True
    product.save()
    return redirect('list_product')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')   
def unlist_product(request,id):
    product=get_object_or_404(Product, id=id)
    product.is_listed=False
    product.save()
    return redirect('list_product')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def edit_product(request,id):
    product=get_object_or_404(Product,id=id)
    categories=Category.objects.all()
    brands=Brand.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        price=request.POST['price']
        category=request.POST['category']
        brand=request.POST['brand']
        features=request.POST['features']
        name_exist=Product.objects.filter(name__iexact=name).exclude(id=product.id).exists()
        if name_exist:
            messages.error(request,f'product {name} is already exists')
        else:
            product.name=name
            product.description=description
            product.price=price
            product.feature=features
            product.category=get_object_or_404(Category,id=category)
            product.brand=get_object_or_404(Brand,id=brand)
            product.save()
            messages.success(request,'product update successfully')
            return redirect('list_product')  
    return render(request,'admin/edit_product.html',{'product':product,'categories':categories,'brands':brands})
    
#======================Product session End=====================# 


#======================Variant session=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_variant(request,id):
    product=get_object_or_404(Product,id=id)
    if request.method=='POST':
        color=request.POST.get('color')
        stock=request.POST.get('stock')
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        if color and stock and image1:  
            Variant.objects.create(
                product=product,
                color=color,
                stock=stock,
                image1=image1,
                image2=image2,
                image3=image3,
            )
            messages.success(request,'variant added successfully')
            return redirect('list_variant',id=product.id)
        else:
            messages.error(request,'All fields are requried')
    return render(request,'admin/add_variant.html')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def view_varient(request,id):
    product = Product.objects.get(id=id)
    variants = Variant.objects.filter(product=product).distinct()
    return render(request,'admin/variant.html',{'variants':variants,'product':product})

#======================Variant session End=====================# 



from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from products.models import Category,Brand,Product,Variant,Subcategory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError



# Create your views here.

User=get_user_model

#======================category  section=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_category(request):
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        category_exists=Category.objects.filter(name__iexact=name).exists()
        if category_exists:
            messages.error(f'The category {name} is already exists')
            return redirect('list_category')
        if name:
            Category.objects.create(
                name=name,
                description=description,
                image=image
            )
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
        image=request.FILES.get('image')
        category_exists=Category.objects.filter(name__iexact=name).exclude(id=category.id).exists()
        if category_exists:
            messages.error(request,f'category{name} already exists')
        else:
            category.name=name
            category.description=description
            if image:
                category.image=image
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

#======================Category  section End=====================# 


#======================Sub_category  section=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_subcategory(request,id):
    category=get_object_or_404(Category,id=id)
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        
        if name:
            subcategory_exists=Subcategory.objects.filter(name__iexact=name,category=category).exclude(id=category.id).exists()
            if subcategory_exists:
                messages.error(request,f'subcategory {name} is already exists under this category ')
            else:
                Subcategory.objects.create(
                    name=name,
                    category=category,
                    description=description,
                    image=image,
                )
                messages.success(request,'Subcategory added successfully')
                return redirect('view_subcategory',id=category.id)
        else:
            messages.error(request,'subcategory name is required!')
            return redirect('view_subcategory.html',id=category.id)
    return render(request,'admin/add_subcategory.html',{'category':category})


@never_cache
@user_passes_test(lambda u: u.is_superuser,login_url='/adminn/')
def view_subcategory(request,id):
    category=get_object_or_404(Category,id=id)
    subcategory=Subcategory.objects.filter(category=category)
    return render(request,'admin/subcategory.html',{'subcategory':subcategory,'category':category})


@never_cache
@user_passes_test(lambda u: u.is_superuser,login_url='/adminn/')
def edit_subcategory(request,id):
    subcategory=get_object_or_404(Subcategory,id=id)
    category=subcategory.category
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        subcategory_exists=Subcategory.objects.filter(name__iexact=name,category=category).exclude(id=subcategory.id).exists()
        if subcategory_exists:
            messages.error(request,f'The subcategory  {name} is already exists')
        else:
            subcategory.name=name
            category=get_object_or_404(Category,id=category.id)
            subcategory.description=description
            if image:
                subcategory.image=image
            subcategory.save()
            messages.success(request,'Subcategory update successfully')
            return redirect('view_subcategory',id=category.id)
    return render(request,'admin/edit_subcategory.html',{'subcategory':subcategory,'category':category})


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def list_subcategory(request,subcategory_id):
    subcategory=get_object_or_404(Subcategory,id=subcategory_id)
    category_id=subcategory.category.id
    subcategory.is_listed=True
    subcategory.save()
    return redirect('view_subcategory',id=category_id)
 

@never_cache
@user_passes_test(lambda u:u.is_superuser, login_url='/adminn/')
def unlist_subcategory(request,subcategory_id):
    subcategory=get_object_or_404(Subcategory,id=subcategory_id)
    category_id=subcategory.category.id
    subcategory.is_listed=False
    subcategory.save()
    return redirect('view_subcategory',id=category_id)

#======================Sub_category section End=====================# 


#======================Brand section=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_brand(request):
    if request.method=='POST':
        name=request.POST.get('name')
        name_exists=Brand.objects.filter(name__iexact=name)
        if name_exists:
            messages.error(request,f'The brand {name} is already exists')
            return redirect('list_brand')
        
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
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def add_products(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    subcategories = Subcategory.objects.filter()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        brand_id = request.POST.get('brand')
        features = request.POST.get('features')

        if not all([name, description, price, category_id, subcategory_id, brand_id]):
            messages.error(request, "All fields are required!")
        else:
            try:
                category = get_object_or_404(Category, id=int(category_id))
                subcategory = get_object_or_404(Subcategory, id=int(subcategory_id))
                brand = get_object_or_404(Brand, id=int(brand_id))
                product_exists = Product.objects.filter(
                    name__iexact=name,
                    category=category,
                    subcategory=subcategory,
                    brand=brand
                ).exists()

                if product_exists:
                    messages.error(request, f"The product '{name}' already exists.")
                else:
                    Product.objects.create(
                        name=name,
                        category=category,
                        subcategory=subcategory,
                        brand=brand,
                        feature=features,
                        price=price,
                        description=description,
                    )
                    messages.success(request, "Product added successfully!")
                    return redirect('list_product')

            except (ValueError, ValidationError) as e:
                messages.error(request, f"Error: {e}")

    return render(request,'admin/addproducts.html',{'categories': categories, 'brands': brands, 'subcategories': subcategories})



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
    subcategory=Subcategory.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        price=request.POST['price']
        category=request.POST['category']
        subcategory=request.POST['subcategory']
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
            product.subcategory=get_object_or_404(Subcategory,id=subcategory)
            product.save()
            messages.success(request,'product update successfully')
            return redirect('list_product')  
    return render(request,'admin/edit_product.html',{'product':product,'categories':categories,'brands':brands,'subcategory':subcategory})
    
#======================Product session End=====================# 


#======================Variant session=====================# 
@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def add_variant(request,id):
    product=get_object_or_404(Product,id=id)
    if request.method=='POST':
        color=request.POST.get('color')
        stock=request.POST.get('stock')
        try:
            stock=int(stock)
            if stock <0:
                messages.error(request,'Enter a valid quantity')
                return redirect('add_variant',id=product.id)
        except ValueError:
            messages.error(request,'Stock quantity must be a valid number')
            return redirect('add_variant',id=product.id)
        
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        variant_exist = Variant.objects.filter(product=product, color__iexact=color).exists()
        if variant_exist:
            messages.error(request,f'variant {color} is already exists')
        else:
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


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def edit_variant(request,id):
    variant=get_object_or_404(Variant,id=id)
    product=variant.product
    if request.method=='POST':
        color=request.POST['color']
        stock=request.POST['stock']
        try:
            stock=int(stock)
            if  stock < 0 :
                messages.error(request,'Enter a valid quantity')
                return redirect('edit_variant',id=variant.id)
        except ValueError:
            messages.error(request,'Stock quantity must be a valid number')
            return redirect('edit_variatnt',id=variant.id)

        image1=request.FILES.get('image1',variant.image1)
        image2=request.FILES.get('image2',variant.image2)
        image3=request.FILES.get('image3',variant.image3)

        variant_exists=Variant.objects.filter(product=product,color__iexact=color).exclude(id=variant.id).exists()
        if variant_exists:
            messages.error(request,f'The variant {color} is already exists')
        else:
            variant.color=color
            variant.stock= stock
            variant.image1=image1
            variant.image2=image2
            variant.image3=image3
            variant.save()
            messages.success(request,'The variant updated successfuly')
            return redirect('list_variant',id=product.id)

    return render(request,'admin/edit_variant.html',{'variant':variant})


@never_cache
@user_passes_test(lambda u:u.is_superuser)
def activate_variant(request,variant_id):
    variant=get_object_or_404(Variant,id=variant_id)
    variant.is_listed=True
    variant.save()
    return redirect('list_variant',id=variant.product.id)

@never_cache
@user_passes_test(lambda u:u.is_superuser)
def deactivate_variant(request,variant_id):
    variant=get_object_or_404(Variant,id=variant_id)
    variant.is_listed=False
    variant.save()
    return redirect('list_variant',id=variant.product.id)


#======================Variant session End=====================# 



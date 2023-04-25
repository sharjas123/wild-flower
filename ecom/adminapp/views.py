from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import  login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import auth
from homeapp.models import Category,Product,ProductImage,User
from cartapp.models import Payment
import os
from .forms import BannerForm
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from cartapp.models import Order
from .models import *
from django.db.models import Sum
from datetime import datetime


def adminlogin(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user =auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,"Username or password incorrect")
    return render(request, 'admin/admin_login.html')   


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def dashboard(request):
    user = User.objects.count()
    category = Category.objects.count()
    product = Product.objects.count()
    order = Order.objects.count()
    delivered_orders = Order.objects.filter(status='Delivered')
    total_income = delivered_orders.aggregate(total=Sum('order_total'))['total'] or 0
    cod_sum = Payment.objects.filter(payment_method='COD').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    razorpay_sum = Payment.objects.filter(payment_method='Paid by Razorpay').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    # total_income = cod_sum + razorpay_sum or 0

    allcategory = Category.objects.all()
    return render(request,'admin/admin_dash.html',locals())


def logout_admin(request):  #logout admin

    auth.logout(request)
    return redirect('adminlogin')

def addcategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        
        
        if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
            messages.info(request, "Category already exists")

        else:
            Category.objects.create(name=name)
            messages.success(request, "Category added successfully")
            return redirect(viewcategory)
    return render(request, 'admin/add_category.html')


def viewcategory(request):
    category = Category.objects.all().order_by('id')   
    dict_user={
        'categories':category
    }
    return render(request, 'admin/view_category.html',dict_user)


def editcategory(request,pid):
    category = Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request,'Category edited successfully')
        return redirect(viewcategory)
    return render(request, 'admin/edit_category.html',locals())


def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.info(request,'Category deleted successfully')
    return redirect(viewcategory)




def addproduct(request):
    category = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        categ = request.POST['categories']
        desc = request.POST['desc']
        images = request.FILES.getlist('image')
        stock = request.POST['stock']
        catobj = Category.objects.get(id=categ)
        product = Product.objects.create(name=name, price=price, category=catobj, description=desc ,stock=stock)
        product.save()
        for image in images:
            ProductImage.objects.create(product=product, images=image)
        messages.success(request, "Product Added")
        return redirect(viewproduct)


    return render(request, 'admin/add_product.html',locals())



def viewproduct(request):
    product = Product.objects.all().order_by('id')
    dict_prod = {
        'product' : product,
    }
    return render(request, 'admin/view_product.html',dict_prod)




@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def editproduct(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    images = ProductImage.objects.filter(product=product)
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        stock = request.POST['stock']
        catobj = Category.objects.get(id=cat)
        
        if int(price) < 0:
            messages.warning(request,"Enter a valid quantity")
            return redirect(editproduct,pid)
        else:

        # Update product attributes
            Product.objects.filter(id=pid).update(name=name, price=price, category=catobj, description=desc ,stock=stock)

        # Get the new images uploaded during editing
        new_images = request.FILES.getlist('images')

        # Add the new images to the product
        for image in new_images:
            ProductImage.objects.create(product=product, images=image)
       
        messages.success(request, "Product Updated")
        return redirect(viewproduct)
    return render(request, 'admin/edit_product.html', locals())

@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def delete_image(request, iid):
    image = ProductImage.objects.get(id=iid)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image.images))
    os.remove(image_path)
    product_id = image.product.id if image.product else None
    image.delete()
    if product_id:
        return HttpResponseRedirect(reverse(editproduct, args=[product_id]))
    else:
        return HttpResponseRedirect(reverse(viewproduct))
    print(f"DEBUG: iid={iid}, image={image}, image_path={image_path}, product_id={product_id}")


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def deleteproduct(request, pid):
    print("hi")
    product = Product.objects.get(id=pid)
    print(product)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect(viewproduct)


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def manageuser(request):
    user = User.objects.all().order_by('id')[1:]

    return render(request, 'admin/manage_user.html', {'user': user})

@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def blockuser(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect(manageuser)


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def manage_order(request):
    orders=Order.objects.all().order_by('id')
    return render(request, 'admin/manage_order.html', locals())


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            # check if banner already exists in database
            if Banner.objects.exists():
                # if banner exists, delete it before adding new banner
                Banner.objects.all().delete()
            form.save()
            # return redirect('banner_list')  # replace with your own URL pattern name
    else:
        form = BannerForm()
    return render(request, 'admin/add_banner.html', {'form': form})




@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def update_order(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST.get('status')
        if(status):
            order.status = status
            order.save()
        if status  == "Delivered":
            try:
                payment = Payment.objects.get(payment_id = order.order_number, status = False)
                print(payment)
                if payment.payment_method == 'Cash on Delivery':
                    payment.paid = True
                    payment.save()
            except:
                pass
    return redirect(manage_order)



def sales_report(request):
    fro=request.GET.get('from_date')
    to=request.GET.get('to_date')
    
    if fro and to :
        orders = Order.objects.all().order_by('-id')
        today_date = datetime.now().strftime('%Y-%m-%d')

        if 'from_date' in request.GET and 'to_date' in request.GET:
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']

            if to_date > today_date:
                messages.warning(request, "Please select a date up to today's date.")
            elif from_date > to_date:
                messages.warning(request, "The from date should be before than the To date")
            else:
                orders = orders.filter(created_at__range=[from_date, to_date])
                total_sales = orders.aggregate(Sum('paid_amount'))['paid_amount__sum']
    else:
        orders = Order.objects.all().order_by('-id')
       
       
    return render(request, 'admin/sales.html',locals())



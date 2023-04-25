from django.shortcuts import render,redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
from adminapp.models import Banner
from cartapp.models import Order
# from cartapp.models import Order
import pyotp
from .forms import UserProfileForm,UserForm

# Create your views here.

def index(request):
    # product=Product.objects.all().order_by('-created')
    banner = Banner.objects.all().first()
    return render(request,'home/index.html',locals())

def error_page(request,exception):
    return render(request,'home/404error.html')


def signin(request):
    return render(request,'home/login.html')

def generate_otp():
    # Generate a random secret key (base32 encoded)
    secret_key = pyotp.random_base32()

    # Create a TOTP object using the secret key
    totp = pyotp.TOTP(secret_key)

    # Generate the OTP
    otp = totp.now()

    return otp

def send_otp_email(email, otp):

    subject = 'OTP for account verification'
    message = f'Your OTP for account verification is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)




def register(request):
    user = None
    if request.method == 'POST':
        # Get form data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        

        # Check if password and confirm password match
        if User.objects.filter(first_name=username).exists():
                messages.info(request,'Username not available!')
                return redirect(register)
        elif User.objects.filter(username=email).exists():
                    messages.info(request,'email entered has an existing account please login to access!')
                    return redirect(register)
        elif password != confirm_password:
                    messages.error(request, 'Passwords do not match')
                    return redirect(register)
        
        else:

        # Generate OTP
            otp = generate_otp()
            print(otp)
        
        # Save user details to database
            
            user = User.objects.create_user(username=email, password=password, first_name=username)
            
        # Send OTP to user email
            send_otp_email(email, otp)


         # Create UserProfile object for the user
            UserProfile.objects.create(user=user)
            
            
        # Save OTP to database
            user.profile.otp = otp
            user.profile.save()
        
        # Redirect to OTP verification page
            return redirect('verifyotp', user.id)

    return render(request, 'home/register.html')



    #OTP verification

def verify_otp(request, user_id):
    print('hi')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp = request.POST['otp']
        if user.profile.otp == otp:
            user.profile.is_verified = True
            user.profile.otp = ''
            user.profile.save()

            messages.success(request, 'Account has been verified')
            username = user.username
            login(request, user)
            messages.success(request, "User login successfull")
            request.session['username'] = username
            return redirect(index)
            
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('verifyotp', user_id)

    return render(request, 'home/verify_otp.html', {'user': user})


#Resend OTP

def resend_otp(request, user_id):
    user = User.objects.get(id=user_id)

    # Generate new OTP
    otp = generate_otp()

    # Send the OTP to the user via email
    send_otp_email(user.username, otp)

    # Save new OTP to database
    user.profile.otp = otp
    user.profile.save()

    messages.success(request, 'New OTP has been sent to your email')
    return redirect('verifyotp', user_id)



def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(username=username, password=password)
       
        if user is not None:
            login(request, user)
            messages.success(request, "User login successfull")
            request.session['username'] = username
            return redirect(index)
        
        else:
             messages.info(request, 'Inavalid Username or password')

    return render(request, 'home/login.html',locals())

 #LOGOUT REQUEST
def logout(request):  

    auth.logout(request)
    return redirect('signin')


def address_book(request):
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_addresses = request.POST.getlist('selected_addresses')
        if selected_addresses is None:
            messages.success(request,"Select an Address")
        else:
            Address.objects.filter(id__in=selected_addresses).delete()
            return redirect(address_book)
    
    return render(request, 'home/addressbook.html', {'addresses': addresses})




def add_address(request,id):
    id=id
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    if request.method == 'POST':
        address = Address(
            user=request.user,
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address_line_1=request.POST['address_line_1'],
            address_line_2=request.POST.get('address_line_2', ''),
            # phone=request.POST['phone'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )
        address.save()

        if id==0 :
            return redirect(address_book)
        else :
            return redirect('checkout')
    else:
        context = {
            'state': state,
            'city': city,
        }
    return render(request, 'home/addaddress.html',context)

def edit_address(request, address_id):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    newaddress = Address.objects.get(id= address_id)
    
    if request.method == 'POST':
        newaddress.firstname=request.POST['firstname']
        newaddress.lastname=request.POST['lastname']
        newaddress.email=request.POST['email']
        newaddress.address_line_1=request.POST['address_line_1']
        newaddress.address_line_2=request.POST.get('address_line_2', '')
        newaddress.phone=request.POST['phone']
        newaddress.city=request.POST['city']
        newaddress.state=request.POST['state']
        newaddress.pincode=request.POST['pincode']
        newaddress.save()
        messages.success(request,"Your Address successfully edited")
        return redirect(address_book)
    
    context = {
        'state': state,
        'city' : city,
        'newaddress' : newaddress
    }

    return render(request, 'home/edit_address.html',context)


def updateprofile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save()
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            user_profile = profile.save()
            messages.info(request, 'Updated Successfully')
            return redirect(user)

    return render(request, 'home/updateuserprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def user(request):
    if request.user.is_authenticated:
        return render(request,'home/user.html')
    else:
        return render(request,'home/login.html')
    

    
def userproduct(request, id):
    if id == 0:
        product = Product.objects.all().order_by('-stock')
    else:
        category = Category.objects.get(id=id)
        product = Product.objects.filter(category=category)
    
    allcategory = Category.objects.all() 
    paginator = Paginator(product, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  
    return render(request, 'home/user_product.html',locals())



def singleproduct(request, id):
    prod = Product.objects.get(id=id)
    images = ProductImage.objects.filter(product_id=id)
    reviews = Review.objects.filter(products=prod)

    if request.method == 'POST':
        if 'username' in request.session:
            feedback = request.POST.get('message')
            user = request.user
            
            review = Review(user=user, feedback=feedback)
            review.save()
            review.products.set([prod])
            messages.info(request,'thank you for your valuable feedback ')  # Use set() to add the product to the relationship
            return redirect('singleproduct', id=id)
        messages.info(request, 'Please login to add your review')
    blog = Product.objects.get(id=id)
    context={
        blog : 'blog',
    }
    return render(request, 'home/user_singleprod_details.html', locals())


def search(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword)).order_by('created')
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    allcategory = Category.objects.all() 
    context = {
        'categories': Category.objects.all(),
        'product': products,
        'keyword' : keyword,
        'allcategory' : allcategory,
        'page_obj': page_obj
        
        
    }
    return render(request, 'home/user_product.html', context)




def user(request):
    if request.user.is_authenticated:
        return render(request,'home/user.html')
    else:
        return render(request,'home/login.html')
    

def orderbook(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'home/myorders.html', {'orders': orders})
from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify





STATE_CHOICES = (
    ('Kerala','Kerala'),
    ('Tamilnadu','Tamilnadu'),
    ('Karnataka','Karnataka'),
    ('AndraPradesh','AndraPradesh')
)
DIST_CHOICES = {
    ('Kannur','Kannur'),
    ('Kozhikkode','Kozhikkode'),
    ('Ernakulam','Ernakulam'),
    ('Thiruvananthapuram','Thiruvananthapuram'),
    ('Banglore','Banglore'),
    ('Hubli','Hubli'),
    ('Hydrabad','Hydrabad'),
    ('Coimbator','Coimbator'),
    ('Madurai','Madurai'),
}

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10, null=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)
    district = models.CharField(choices=DIST_CHOICES,max_length=20, null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=20, null=True)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.PositiveIntegerField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username






class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    stock = models.PositiveIntegerField(null=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    slug = models.CharField(max_length=1000,null=True,blank=True)


    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name+"-"+str(self.updated))
        return super().save(*args, **kwargs)




class ProductImage(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    images = models.ImageField(upload_to='media',null=True)

    def __str__(self):
        return self.product.name
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=200)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.CharField(validators=[phone_regex], max_length=10, null=True)
    city = models.CharField(choices=DIST_CHOICES,max_length=255)
    state = models.CharField(choices=STATE_CHOICES,max_length=255)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.username
    


class Review(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(null=True, blank=True)



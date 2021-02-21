from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission

from product.models import Product
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User modal for SuperUser, Admin, Seller, Buyer"""
    class GenderChoices(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHERS = 'O', _('Others')

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mobile_no = models.CharField(unique=True, null=True,  max_length=10)
    country_code = models.CharField(max_length=5, default="+91")
    address_line_1 = models.CharField(max_length=300, blank=True, null=True)
    address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")
    aadhar_no = models.CharField(blank=True, null=True, max_length=12)
    pan_no = models.CharField(blank=True, null=True, max_length=10)
    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # To verify user Phone Number
    is_seller = models.BooleanField(default=False)  # check whether user is bullon dealer
    is_admin = models.BooleanField(default=False)  # check whether user is admin
    login_otp = models.CharField(max_length=10, blank=True, null=True)  # Stores Otp for the Verification
    timestrap = models.DateTimeField(blank=True, null=True)
    # Might Required another attribute for login and verifying.
    # every user should be active or super admin has disabled his account.
    is_active = models.BooleanField(default=True)
    favourites = models.ManyToManyField('User', related_name='Fauorites', blank=True)
    # For Django Admin Panel
    is_staff = models.BooleanField(default=False)
    is_detailed = models.BooleanField(default=False)  # To check whether he has filled all the inforamtion.

    objects = UserManager()

    REQUIRED_FIELDS = ['name', 'email']
    USERNAME_FIELD = 'mobile_no'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Company(models.Model):
    """To store the detail about the company of a User """

    user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='Company_fk_User', blank=True, null=True)
    company_name = models.CharField(max_length=200)
    company_type = models.ForeignKey(
        'CompanyType', on_delete=models.SET_NULL, blank=True, null=True)
    company_pan_no = models.BigIntegerField(blank=True, null=True)
    cin_no = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    def __repr__(self):
        return self.company_name


class CompanyType(models.Model):
    """To store the Company Like. Pvt Lmtd., Firm, Etc. """
    company_type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.company_type_name

    def __repr__(self):
        return self.company_type_name


class CompanyBranchDetail(models.Model):
    """To Store the Detail of a Store of a company """
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='Company_Name')
    mobile_no1 = models.BigIntegerField(blank=True, null=True)
    mobile_no2 = models.BigIntegerField(blank=True, null=True)
    gst_no = models.BigIntegerField(blank=True, null=True)
    geo_latitude = models.TextField(blank=True, null=True)
    geo_longitude = models.TextField(blank=True, null=True)
    branch_address_line_1 = models.CharField(max_length=300, blank=True, null=True)
    branch_address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    branch_city = models.CharField(max_length=100, blank=True, null=True)
    branch_pincode = models.CharField(max_length=6, blank=True, null=True)
    branch_state = models.CharField(max_length=100, blank=True, null=True)
    branch_country = models.CharField(max_length=100, blank=True, default='India')
    is_active = models.BooleanField(default=True)
    is_permitted = models.BooleanField(default=False)
    is_analytical = models.BooleanField(default=False,  blank=True)
    delivery_time = models.CharField(max_length=128, null=True, blank=True)
    min_value = models.CharField(max_length=128, null=True, blank=True)
    cash_percentage = models.CharField(max_length=128, null=True, blank=True)
    permission_date = models.DateTimeField(null=True, blank=True)
    permission_last_date = models.DateTimeField(null=True, blank=True)
    is_detailed = models.BooleanField(default=False)  # To check whether he has filled all the inforamtion.

    def __str__(self):
        return f"{self.company.company_name} - {self.branch_city}"

    def __repr__(self):
        return f"{self.company.company_name} - {self.branch_city}"


class SendMessageDetail(models.Model):
    id = models.BigIntegerField(primary_key=True)
    message_content = models.TextField(blank=True, null=True)
    current_date = models.DateTimeField(auto_now_add=True)
    is_detailed = models.BooleanField(default=False)
    name = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return f"{self.name}"
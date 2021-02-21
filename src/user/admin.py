from django.contrib import admin
from .models import (
    User,
    Company,
    CompanyBranchDetail,
    CompanyType,
    SendMessageDetail
)
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin


admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanyBranchDetail)
admin.site.register(CompanyType)
admin.site.register(Permission)
admin.site.register(SendMessageDetail)

# exclude = ['login_otp', 'is_superuser']
# fieldsets = (
#     (None,
#      {
#          'fields':
#          ('name', 'email', 'mobile_no', 'password', 'father_name', 'gender', 'address_line_1', 'address_line_2',
#           'city', 'pincode', 'state', 'country', 'aadhar_no', 'is_admin', 'is_staff')}),
#     ('Advanced options',
#      {'classes': ('collapse',),
#       'fields': ('is_verified', 'is_seller', 'pan_no'), }),)

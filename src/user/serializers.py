from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import validators
from datetime import datetime

from user.models import Company, CompanyBranchDetail, User, CompanyType, Group,SendMessageDetail
from . import models


class UserRegisterSerializer(serializers.ModelSerializer):
    """To Register a user"""
    firm_name = serializers.CharField(write_only=True)
    mobile_no = serializers.IntegerField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    is_seller = serializers.BooleanField(required=True)
    country_code = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    city = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id", "name", "country_code", 'country', 'state', 'city',
                  "mobile_no", "password", "firm_name", "is_seller")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            name=validated_data["name"],
            mobile_no=validated_data['mobile_no'],
            city=validated_data['city'],
            state=validated_data['state'],
            country=validated_data['country'],
            is_seller=validated_data['is_seller'],
            timestrap=datetime.now()
        )

        user.set_password(validated_data["password"])
        user.save()

        if validated_data['is_seller']:
            company = Company(user_id=user, company_name=validated_data['firm_name'])
            company.save()
            company_branch_details = CompanyBranchDetail(company=company)
            company_branch_details.save()

        return user


class UserVerifyOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(write_only=True)


class UserSendLoginOTPSerializer(serializers.Serializer):
    mobile_no = serializers.IntegerField(write_only=True)


class UserVerifyLoginOTPSerializer(serializers.Serializer):
    mobile_no = serializers.IntegerField(write_only=True)
    otp = serializers.IntegerField(write_only=True)


class UserSendForgotPasswordOTPSerializer(serializers.Serializer):
    mobile_no = serializers.IntegerField(write_only=True)


class UserVerifyForgotPasswordOTPSerializer(serializers.Serializer):
    mobile_no = serializers.IntegerField(write_only=True)
    otp = serializers.IntegerField(write_only=True)


class UserPasswordResetSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

# ============================ Profile Serializers ==================================


class CompanyDetailsForUserSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta():
        model = CompanyBranchDetail
        fields = ['company', 'branch_address_line_1', 'branch_address_line_2', 'branch_city',
                  'branch_state', 'branch_country', 'is_permitted', 'permission_date', 'permission_last_date']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['name', 'mobile_no', 'is_verified', 'is_seller', 'is_active','is_admin']

# ============================ Personal Serializers ==================================


class UserPersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['name', 'mobile_no', 'address_line_1', 'address_line_2', 'city', 'pincode', 'state', 'country']


# ============================ Company Serializers ==================================


class UserDetailsForCompanySerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['is_seller', 'is_active']
        read_only_fields = ['is_seller', 'is_active']


class UserCompanyNameSerializer(serializers.ModelSerializer):
    class Meta():
        model = Company
        fields = ['company_name']


class UserCompanyDetailsSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta():
        model = CompanyBranchDetail
        fields = ['company', 'mobile_no1', 'mobile_no2', 'branch_address_line_1', 'branch_address_line_2', 'branch_city',
                  'branch_pincode', 'branch_state', 'branch_country', 'is_permitted', 'permission_date', 'permission_last_date']
        read_only_fields = ['is_permitted', 'permission_date', 'permission_last_date']

# ============================ Setting Serializers ==================================


class UserDetialsForSettingsSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'is_seller', 'is_active']
        read_only_fields = ['id', 'is_seller', 'is_active']


class UserSettingDetailsSerializer(serializers.ModelSerializer):
    class Meta():
        model = CompanyBranchDetail
        fields = ['is_analytical', 'is_permitted', 'delivery_time', 'min_value',
                  'cash_percentage', 'permission_date', 'permission_last_date']
        read_only_fields = ['is_analytical', 'is_permitted', 'permission_date', 'permission_last_date']


# ============================ Business Serializers ==================================

class UserDetialsForBusinessSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['is_seller', 'name', 'father_name', 'mobile_no', 'address_line_1',
                  'address_line_2', 'city', 'pincode', 'state', 'email', 'aadhar_no', 'pan_no', 'is_active']
        read_only_fields = ['is_seller', 'is_active']


class CompanyDetailsForBusinessSerializer(serializers.ModelSerializer):
    company_type_input = serializers.CharField(write_only=True)
    company_type = serializers.StringRelatedField()

    class Meta():
        model = Company
        fields = ['company_name', 'company_type', 'company_pan_no', 'cin_no', 'company_type_input']


class UserBusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta():
        model = CompanyBranchDetail
        fields = ['mobile_no1', 'mobile_no2', 'gst_no']

    # ---------------------------------- COMPANY TYPE -----------------------------------------


class CompanyTypeDetailsSerializer(serializers.ModelSerializer):
    class Meta():
        model = CompanyType
        fields = '__all__'

    # ---------------------------------- END COMPANY TYPE -----------------------------------------


# ======================================== Geolocation settings ========================================

class UserGeolocationDetailsSerailzer(serializers.ModelSerializer):
    class Meta():
        model = CompanyBranchDetail
        fields = ['geo_latitude', 'geo_longitude']


# ============================ Reset Profile Password Serializers ==================================

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================             Super Admin Serializers           ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# ============================ User List Serializers ==================================

class UserListSerailizer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'name', 'mobile_no', 'city', 'is_seller', 'is_admin', 'timestrap']


# ============================ User Preview  Serializers ==================================

class CompanyDetailsForUserPreviewSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta():
        model = CompanyBranchDetail
        fields = ['company', 'branch_city',
                  'branch_state', 'branch_country', 'is_permitted', 'permission_date', 'permission_last_date']
        read_only_fields = ['company', 'branch_city',
                            'branch_state', 'branch_country', 'permission_date', 'permission_last_date']

        extra_kwargs = {'is_permitted': {'required': True}}


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'name', 'email', 'mobile_no', 'is_verified', 'is_seller', 'is_active']
        read_only_fields = ['id', 'name', 'email', 'mobile_no', 'is_verified', 'is_seller']

        extra_kwargs = {'is_active': {'required': True}}


# ============================ Admin Preview  Serializers ==================================
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': False},
        }
        read_only_fields = ['name']


class AdminPreviewSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta():
        model = User
        fields = ['id', 'name', 'email', 'mobile_no', 'city', 'state', 'country', 'is_verified', 'is_admin',
                  'is_active', 'groups', ]
        read_only_fields = ['is_verified', 'is_admin', 'groups', 'is_active']


# ============================ Admin Registration Serializers ==================================

class AdminRegistrationSerailizer(serializers.ModelSerializer):
    """ To Create Admin User From Super User """

    name = serializers.CharField(required=True)
    mobile_no = serializers.IntegerField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(required=True)
    country_code = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta():
        model = User
        fields = ("id", "name", 'email', "mobile_no", "password", "country_code",
                  'country', 'state', 'city', 'is_admin')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            name=validated_data["name"],
            mobile_no=validated_data['mobile_no'],
            email=validated_data['email'],
            city=validated_data['city'],
            state=validated_data['state'],
            country=validated_data['country'],
            is_admin=True,
            timestrap=datetime.now()
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class SendMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SendMessageDetail
        fields = ['id','name', 'message_content','current_date','is_detailed']
        

# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================             Dummy Serializers                 ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# ============================ Dummy Serializer for add Company branch details ==================================

class DummyBranchDetailsSerializer(serializers.ModelSerializer):
    class Meta():
        model = CompanyBranchDetail
        exclude = ['gst_no', 'geo_latitude', 'geo_longitude', 'is_analytical']

import json
from django.core import serializers
from django.conf import settings
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from user.models import User


from . import serializers as user_serializers
from . import utils
from . import models
from . import permissions
from . import paginations


# ===================================== User to send login otp ======================================================

class UserSendLoginOtpAPIView(views.APIView):
    # TODO : "Permission Set"
    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserSendLoginOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.validated_data.get('mobile_no')
            if utils.send_otp(mobile_no):
                print("Sended Login Otp")
                return Response({"message": "OTP SENDED"}, status=status.HTTP_200_OK)
            return Response({"message": "Username is invalid"}, status=status.HTTP_400_BAD_REQUEST)


# ===================================== User to verify login otp ======================================================

class UserVerifyLoginOtpAPIView(views.APIView):
    # TODO : "Permission Set"
    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserVerifyLoginOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.validated_data.get('mobile_no')
            login_otp = serializer.validated_data.get('otp')
            is_login_otp_correct = utils.verify_otp(mobile_no, login_otp)
            if is_login_otp_correct:
                user = User.objects.get(mobile_no=mobile_no)
                return Response(utils.get_tokens_for_user(user), status=status.HTTP_200_OK)
            return Response({'message': "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


# ===================================== User to verify his phone number via otp sending ======================================================

class UserSendVerificationOTPAPIView(views.APIView):
    # TODO : "Permission Set"
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        mobile_no = request.user.mobile_no
        if not request.user.is_verified:
            utils.send_otp(mobile_no)
            return Response({"message": "Verification OTP sended"})
        return Response({"message": "User is already Verified"})


# ===================================== User to verify his phone number via otp verifying with phone number =========================================

class UserVerifyOTPAPIView(views.APIView):
    # TODO : "Permission Set"
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserVerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            verification_otp = serializer.validated_data.get('otp')
            mobile_no = request.user.mobile_no
            is_user_verified = utils.verify_otp(mobile_no, verification_otp)
            if is_user_verified:
                User.objects.filter(mobile_no=mobile_no).update(is_verified=True)
                return Response({"message": "OTP Verified Successfully"})
            else:
                return Response({"message": "Error in OTP Verification"})


# ======================================  User Details after the user login ===============================================

class UserDetailAPIView(views.APIView):
    # TODO : "Permission Set"
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = serializers.serialize(
            'json',
            [request.user],
            fields=('name', 'email', 'mobile_no', 'is_verified', 'is_seller', 'is_admin', 'is_superuser')
        )
        data = json.loads(data)
        return Response({"user": data[0]['fields']})


# ============================================ User forgot password in the login view ===============================================

class UserSendForgotPasswordOTPAPIView(views.APIView):
    # TODO : "Permission Set"
    """ Sends Otp to User for Forget password """

    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserSendForgotPasswordOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.validated_data.get('mobile_no')
            if utils.send_otp(mobile_no):
                return Response({"message": "OTP SENDED"}, status=status.HTTP_200_OK)
            return Response({"message": "Username is invalid"}, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyForgotPasswordOTPAPIView(views.APIView):
    # TODO : "Permission Set"
    """ Verify Otp of User for Forget password """

    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserVerifyForgotPasswordOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_no = serializer.validated_data.get('mobile_no')
            forget_password_otp = serializer.validated_data['otp']
            is_forgot_pass_otp_correct = utils.verify_otp(mobile_no, forget_password_otp)
            if is_forgot_pass_otp_correct:
                return Response({'message': 'Forgot Password OTP verified'}, status=status.HTTP_200_OK)
            return Response({'message': "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetAPIView(views.APIView):
    # TODO : "Permission Set"
    """ Reset the password of the user """

    def post(self, request, *args, **kwargs):
        serializer = user_serializers.UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            user = User.objects.get(mobile_no=serializer.validated_data.get('mobile_no'))
            user.set_password(serializer.validated_data.get("password"))
            user.save()
            return Response({'message': 'Reset Password Successfully Done'}, status=status.HTTP_200_OK)
        return Response({'message': "Reset Password Not Succesfull"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    """ User Profile View """
    # TODO : "Permission Set"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        serializer = user_serializers.UserProfileSerializer(user_queryset)
        company = models.Company.objects.get(user_id=self.request.user)
        company_branch_details_queryset = models.CompanyBranchDetail.objects.get(company=company)
        company_details_serializer = user_serializers.CompanyDetailsForUserSerializer(company_branch_details_queryset)
        return Response(
            {'user_details': serializer.data, 'company_details': company_details_serializer.data},
            status=status.HTTP_201_CREATED)


class UserPersonalDetailsView(views.APIView):
    # TODO : "Permission and To Edit Permission"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        serializer = user_serializers.UserPersonalDetailsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        serializer = user_serializers.UserPersonalDetailsSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer)
            serializer.save()
            return Response({'message': 'Succesfully Update Profile'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCompanyDetailsView(views.APIView):
    # TODO : "Permission and To Edit Permission"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        user_queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        serializer = user_serializers.UserDetailsForCompanySerializer(user_queryset)
        company = models.Company.objects.get(user_id=self.request.user)
        company_branch_details_queryset = models.CompanyBranchDetail.objects.get(company=company)
        company_details_serializer = user_serializers.UserCompanyDetailsSerializer(company_branch_details_queryset)
        return Response(
            {'user_details': serializer.data, 'company_details': company_details_serializer.data},
            status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):

        company_queryset = models.Company.objects.get(user_id=request.user)
        company_branch_queryset = models.CompanyBranchDetail.objects.get(company=company_queryset)
        compnay_branch_serializer = user_serializers.UserCompanyDetailsSerializer(
            company_branch_queryset, data=request.data)
        company_serializer = user_serializers.UserCompanyNameSerializer(company_queryset, data=request.data)
        if compnay_branch_serializer.is_valid(
                raise_exception=True) and company_serializer.is_valid(
                raise_exception=True):
            compnay_branch_serializer.save()
            company_serializer.save()

            return Response({'message': 'Succesfully Update Comapny Profile'})
        return Response(compnay_branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSettingDetailsView(views.APIView):
    # TODO : "Permission and To Edit Permission"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        serializer = user_serializers.UserDetialsForSettingsSerializer(user_queryset)
        company = models.Company.objects.get(user_id=self.request.user)
        company_branch_details_queryset = models.CompanyBranchDetail.objects.get(company=company)
        company_details_serializer = user_serializers.UserSettingDetailsSerializer(company_branch_details_queryset)
        return Response(
            {'user_details': serializer.data, 'company_details': company_details_serializer.data},
            status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        company_queryset = models.Company.objects.get(user_id=request.user)
        company_branch_queryset = models.CompanyBranchDetail.objects.get(company=company_queryset)
        serializer = user_serializers.UserSettingDetailsSerializer(company_branch_queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Succesfully Update Settings Profile'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyTypeDetailsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        company_type_queryset = models.CompanyType.objects.all()
        serializer = user_serializers.CompanyTypeDetailsSerializer(company_type_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO : " Change it to put "

    def post(self, request, *args, **kwargs):
        serializer = user_serializers.CompanyTypeDetailsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBusinessDetailsView(views.APIView):
    # TODO : "Permission and To Edit Permission"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        serializer = user_serializers.UserDetialsForBusinessSerializer(user_queryset)
        company = models.Company.objects.get(user_id=self.request.user)
        company_serializer = user_serializers.CompanyDetailsForBusinessSerializer(company)
        company_branch_details_queryset = models.CompanyBranchDetail.objects.get(company=company)
        company_details_serializer = user_serializers.UserBusinessDetailsSerializer(company_branch_details_queryset)
        return Response(
            {'user_details': serializer.data, 'company': company_serializer.data,
             'company_branch_details': company_details_serializer.data},
            status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user_queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        user_serializer = user_serializers.UserDetialsForBusinessSerializer(user_queryset, data=self.request.data)

        company_queryset = models.Company.objects.get(user_id=self.request.user)
        company_serializer = user_serializers.CompanyDetailsForBusinessSerializer(
            company_queryset, data=self.request.data)

        company_branch_queryset = models.CompanyBranchDetail.objects.get(company=company_queryset)
        company_branch_serializer = user_serializers.UserBusinessDetailsSerializer(
            company_branch_queryset, data=self.request.data)

        if user_serializer.is_valid(
                raise_exception=True) and company_serializer.is_valid(
                raise_exception=True) and company_branch_serializer.is_valid(
                raise_exception=True):

            company_type_query = models.CompanyType.objects.get(
                pk=company_serializer.validated_data.get('company_type_input'))

            user_serializer.save()
            company_serializer.save(company_type=company_type_query)
            company_branch_serializer.save()
            return Response({'message': 'Succesfully Update Business Profile'})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetProfilePasswordView(views.APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = user_serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            old_password = serializer.validated_data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": "Wrong password."},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()
            return Response({'message': 'Password Sucessfully Changed'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGeolocationDetailsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        company_queryset = models.Company.objects.get(user_id=request.user)
        company_branch_queryset = models.CompanyBranchDetail.objects.get(company=company_queryset)
        serializer = user_serializers.UserGeolocationDetailsSerailzer(company_branch_queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        company_queryset = models.Company.objects.get(user_id=request.user)
        company_branch_queryset = models.CompanyBranchDetail.objects.get(company=company_queryset)
        serializer = user_serializers.UserGeolocationDetailsSerailzer(company_branch_queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Geolocation Sucessfully Changed'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMessageNotificationView(views.APIView):
    def get(self,request):
        getNotifications = models.SendMessageDetail.objects.all().order_by('-current_date')
        serializer = user_serializers.SendMessageSerializer(getNotifications, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer =  user_serializers.SendMessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class UpdateUserMessageNotificationView(views.APIView):
    def put(self, request,id):
        notificatons = models.SendMessageDetail.objects.get(id=id)
        serializer = user_serializers.SendMessageSerializer(notificatons, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Message Update Sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================              Super Admin Views                ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# =============================== User List View For Super Admin Only ========================================

class UserListViewForSuperAdmin(generics.ListAPIView):
    # TODO : "Verify the user is superadmin and admin "
    queryset = models.User.objects.filter(is_active=True, is_superuser=False)
    serializer_class = user_serializers.UserListSerailizer
    permission_classes = [IsAuthenticated, permissions.IsSuperAdminOrAdmin]
    pagination_class = paginations.UserLimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', '=mobile_no']

    def get_filter_attribute(self, filtering: str):
        user_filter = {
            'admin': [('is_admin', True), ("is_seller", False)],  # ask , ("is_seller", False)
            'seller': [('is_admin', False), ("is_seller", True), ("is_verified", True)],
            'user': [("is_admin", False), ("is_seller", True)],
            'deleted': [("is_active", False)],
            'permit': [('is_admin', False), ("is_seller", True), ("is_verified", True)]
        }
        if not user_filter.get(filtering.lower()):
            return False
        return user_filter.get(filtering.lower())

    def get_queryset(self):
        if utils.check_permission(request=self.request, permissions=['user.view_user']):
            queryset = super(UserListViewForSuperAdmin, self).get_queryset()
            get_parameter = self.request.query_params
            if get_parameter and get_parameter.get('status'):
                condition = self.get_filter_attribute(get_parameter.get('status'))
                print(condition)
                if not condition:
                    raise ValidationError(detail={'message': 'Invalid Params'})
                queryset = queryset.filter(**dict(condition))
                print(queryset)
                if self.request.user.is_admin:
                    queryset = queryset.filter(is_admin=False)
                    print(queryset)

                # ===================== For seller list ==========================

                if get_parameter.get('status').lower() == 'seller':
                    company_branch_list = models.CompanyBranchDetail.objects.filter(
                        is_permitted=True,
                    )
                    user_list = []
                    for company_branch in company_branch_list:
                        if (
                            company_branch.company.user_id.is_active and
                            company_branch.company.user_id.is_seller and
                            company_branch.company.user_id.is_verified and
                            not company_branch.company.user_id.is_admin
                        ):
                            user_list.append(company_branch.company.user_id)
                    return models.User.objects.filter(name__in=user_list).order_by('timestrap')

                # ===================== List of seller to grant permision for bullion list ==========================

                if get_parameter.get('status').lower() == 'permit':
                    # TODO : Produce all the list of user who are not access to add bullion
                    company_branch_list = models.CompanyBranchDetail.objects.filter(
                        is_permitted=False,
                        is_active=True,
                        is_detailed=True,
                        company__user_id__is_detailed=True
                    )
                    user_list = []
                    for company_branch in company_branch_list:
                        if (
                            company_branch.company.user_id.is_active and
                            company_branch.company.user_id.is_seller and
                            company_branch.company.user_id.is_verified and
                            not company_branch.company.user_id.is_admin
                        ):
                            user_list.append(company_branch.company.user_id)
                    return models.User.objects.filter(name__in=user_list).order_by('timestrap')
            return queryset.order_by('timestrap')


class UserPreviewView(views.APIView):

    permission_classes = [IsAuthenticated, permissions.IsSuperAdminOrAdmin, permissions.IsVerified]

    def get(self, request, *args, **kwargs):
        if utils.check_permission(request=self.request, permissions=['user.view_user']):
            try:
                user_queryset = models.User.objects.get(pk=kwargs['id'])
            except:
                return Response({"message": "Wrong Qurried"}, status=status.HTTP_400_BAD_REQUEST)
            if not user_queryset.is_admin and not user_queryset.is_superuser:
                user_serializer = user_serializers.UserPreviewSerializer(user_queryset)

                try:
                    company_branch_details_queryset = models.CompanyBranchDetail.objects.get(
                        company__user_id=user_queryset)

                    company_branch_serailizer = user_serializers.CompanyDetailsForUserPreviewSerializer(
                        company_branch_details_queryset)
                    return Response(
                        {"user_details": user_serializer.data, "Company_details": company_branch_serailizer.data},
                        status=status.HTTP_201_CREATED)
                except:
                    return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message": "Wrong Query"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        if utils.check_permission(request=self.request, permissions=['user.change_user']):
            try:
                user_queryset = models.User.objects.get(pk=kwargs['id'])
            except:
                return Response({"message": "Wrong Qurried"}, status=status.HTTP_400_BAD_REQUEST)

            user_serializer = user_serializers.UserPreviewSerializer(user_queryset, data=request.data)

            if user_queryset.is_admin or user_queryset.is_superuser:
                return Response({"message": "Wrong Query"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if user_queryset.is_seller:
                    company_branch_queryset = models.CompanyBranchDetail.objects.get(company__user_id=user_queryset)
                    company_branch_serializer = user_serializers.CompanyDetailsForUserPreviewSerializer(
                        company_branch_queryset, data=self.request.data)
                    if company_branch_serializer.is_valid(raise_exception=True):
                        if not user_queryset.is_verified:
                            return Response(
                                {'message': "User is not verified"},
                                status=status.HTTP_400_BAD_REQUEST)
                        company_branch_serializer.save()
                    else:
                        return Response(
                            company_branch_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
                    return Response({'message': 'Profile Sucessfully Changed'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                raise ValidationError(detail=str(e))

            return Response(user_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPreviewView(views.APIView):

    permission_classes = [IsAuthenticated, permissions.IsSuperAdmin]

    def get(self, request, *args, **kwargs):
        try:
            queryset = models.User.objects.get(pk=kwargs['id'])
        except:
            return Response({"message": "Wrong Qurried"}, status=status.HTTP_400_BAD_REQUEST)
        if queryset.is_admin and not queryset.is_superuser:
            serializer = user_serializers.AdminPreviewSerializer(queryset)
            print(queryset.groups.all())
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response({"message": "Wrong Query"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            queryset = models.User.objects.get(pk=kwargs['id'])

            get_parameter = self.request.query_params.get('edit')

            if not get_parameter in ['profile', 'status']:
                return Response({'message': 'Not a good request.'}, status=status.HTTP_400_BAD_REQUEST)

            if get_parameter.lower() == "profile":
                if queryset.is_admin and not queryset.is_superuser:
                    serializer = user_serializers.AdminPreviewSerializer(queryset, data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({'message': "Updated Admin Details"}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Wrong Query"}, status=status.HTTP_400_BAD_REQUEST)

            elif get_parameter.lower() == "status":
                group_queryset = models.Group.objects.all()
                if queryset.is_admin and not queryset.is_superuser:
                    data = self.request.data

                    # serializer = user_serializers.AdminPreviewSerializer(queryset, data=request.data)
                    if not (isinstance(data['groups_id'], list) and all(isinstance(x, int) for x in data['groups_id'])):
                        raise ValidationError(
                            detail={'details': "Send the groups_id in list format and it should be interger"})

                    queryset.groups.clear()
                    # Validate the list number are in the range of group id.
                    group_start_range, group_end_range = 1, len(models.Group.objects.all())+1
                    input_list = data['groups_id']
                    ans = all(ele >= group_start_range and ele < group_end_range for ele in input_list)
                    if ans:
                        queryset.groups.add(*data['groups_id'])
                        queryset.is_active = data['is_active']
                        queryset.save()
                        return Response({'message': "Updated Admin Details"}, status=status.HTTP_201_CREATED)
                    return Response({"message": "Enter the correct group id"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Wrong Query"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise ValidationError(detail={'details': e})


class AdminEditView(views.APIView):

    permission_classes = [IsAuthenticated, permissions.IsAdmin]

    def get(self, request, *args, **kwargs):
        queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        data = {
            'name': queryset.name,
            'mobile_no': queryset.mobile_no,
            'email': queryset.email,
        }
        return Response(data=data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, *args, **kwargs):
        queryset = models.User.objects.get(mobile_no=self.request.user.mobile_no)
        data = self.request.data
        if not self.request.user.is_verified:
            queryset.mobile_no = data['mobile_no']

        if data.get('password'):
            queryset.set_password(data.get('password'))
        queryset.email = data['email']
        queryset.save()
        return Response({'message': "Updated Sucessfully"})


class PermissionGroupListView(views.APIView):
    # TODO : "Verify the user is superadmin and admin "
    permission_classes = [IsAuthenticated, permissions.IsSuperAdminOrAdmin]

    def get(self, request, *args, **kwargs):
        groups = models.Group.objects.all()
        data = []
        for group in groups:
            permission_list = group.permissions.all()
            data.append({
                "id": group.id,
                "name": group.name,
                "permissions": [permission.codename for permission in permission_list]
            })
        return Response(data)


class SendMessageView(views.APIView):
    # TODO : Check whether to add permission.
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        print(data)
        id = data.get('id')
        message = data.get('message')
        try:
            queryset = models.User.objects.get(pk=id)
        except Exception as e:
            raise ValidationError(str(e))
        if message:
            if utils.send_message(mobile=queryset.mobile_no, message=message):
                return Response({'message': ' Message sent Successfully.'}, status=status.HTTP_202_ACCEPTED)
            raise ValidationError(detail={'details': 'Send correct phone number and message'})
        raise ValidationError(detail={'details': " Fill the Id and the message fields."})


# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================             Dummy Views                       ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# ============================ Dummy Views for add Company branch details ==================================


class DummyBranchDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = user_serializers.DummyBranchDetailsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            company_querset = models.Company.objects.get(user_id=self.request.user)
            serializer.save(company=company_querset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error(), status=status.HTTP_400_BAD_REQUEST)

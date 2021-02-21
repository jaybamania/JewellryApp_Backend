from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


from . import views
from .viewsets import UserRegisterViewSet, AdminRegisterViewSet

router = DefaultRouter()
router.register('register', UserRegisterViewSet)
router.register('register/admin', AdminRegisterViewSet)

urlpatterns = [
    path("detail/", views.UserDetailAPIView.as_view(), name="user_detail"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sendloginotp/', views.UserSendLoginOtpAPIView.as_view(), name='send_login_otp'),
    path('loginwithotp/', views.UserVerifyLoginOtpAPIView.as_view(), name="login_with_otp"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('sendotp/', views.UserSendVerificationOTPAPIView.as_view()),
    path('verifyotp/', views.UserVerifyOTPAPIView.as_view()),
    path('forgotpass/sendotp/', views.UserSendForgotPasswordOTPAPIView.as_view(), name='send_forgot_password_otp'),
    path('forgotpass/verifyotp/', views.UserVerifyForgotPasswordOTPAPIView.as_view(), name='verify_forgot_password_otp'),
    path('resetpass/', views.UserPasswordResetAPIView.as_view(), name='reset_password'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('personaldetails/', views.UserPersonalDetailsView.as_view(), name='perosnal_detials'),
    path('companydetails/', views.UserCompanyDetailsView.as_view(), name='company_details'),
    path('settingdetails/', views.UserSettingDetailsView.as_view(), name='Setting_details'),
    path('businessdetails/', views.UserBusinessDetailsView.as_view(), name='Business_details'),
    path('geolocationdetails/', views.UserGeolocationDetailsView.as_view(), name='Geolocation_Details'),
    path('profileresetpass/', views.ResetProfilePasswordView.as_view(), name='Reset_Password'),
    path('details/companytype/', views.CompanyTypeDetailsView.as_view(), name='Company Type details'),
    path('send/message/', views.SendMessageView.as_view(), name="Send Message "),
    path('message/notifications/', views.UserMessageNotificationView.as_view(), name="Message Notifications"),
    path('message/notifications/<int:id>/', views.UpdateUserMessageNotificationView.as_view(), name="Update Notifications"),


    # =================================== Super- Admin - Urls ======================================

    path('list/', views.UserListViewForSuperAdmin.as_view(), name='User List'),
    path('groups/', views.PermissionGroupListView.as_view(), name='Permission Group List'),
    path('list/<int:id>/', views.UserPreviewView.as_view(), name="User Preview"),
    path('admin/<int:id>/', views.AdminPreviewView.as_view(), name="Admin Preview"),
    path('admin/edit/', views.AdminEditView.as_view(), name="Admin Edit"),

    # =================================== Dummy Urls ======================================
    path('dummybranchdetyails/', views.DummyBranchDetailView.as_view(), name='Dummy Branch Details'),

]

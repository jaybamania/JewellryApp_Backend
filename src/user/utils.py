import datetime
import random
import json
from user.models import User
from .message_api import aws_api
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import ValidationError


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_messageOTP_to_db(mobile_no, new_otp, user):
    message = f"OTP for Apps_name application is {new_otp}. OTP's are SECRET. DO NOT disclose it to anyone. We NEVER asks for OTP."
    if aws_api(phone_no=mobile_no, message=message) == str(200):
        current_time = datetime.datetime.now()
        login_otp_data = [new_otp, current_time.strftime("%m/%d/%Y, %H:%M:%S")]
        print(json.dumps(login_otp_data))
        user.login_otp = json.dumps(login_otp_data)
        user.save()
        return True
    return False


def send_message(mobile, message):
    if aws_api(phone_no=mobile, message=message) == str(200):
        return True
    return False


# function to generate OTP


def generateOTP():
    return random.randint(100000, 999999)


def send_otp(mobile_no):
    """Will send the OTP to user mobile no"""
    users = User.objects.filter(mobile_no=mobile_no)
    if users.exists():
        user = users[0]
        new_otp = generateOTP()
        old_otp = user.login_otp

        if old_otp is None:
            # for counter method otp
            return send_messageOTP_to_db(mobile_no=mobile_no, new_otp=new_otp, user=user)

        else:
            old_otp = json.loads(old_otp)
            old_time = datetime.datetime.strptime(old_otp[1], "%m/%d/%Y, %H:%M:%S")
            if (datetime.datetime.now() - old_time).total_seconds() > 180:
                return send_messageOTP_to_db(mobile_no=mobile_no, new_otp=new_otp, user=user)

            else:
                return aws_api(phone_no=mobile_no, otp=old_otp[0]) == str(200)


def verify_otp(mobile_no, login_otp):
    users = User.objects.filter(mobile_no=mobile_no)
    if users.exists():
        user = users[0]
        # TODO: change the otp type form the modal to int
        old_otp = user.login_otp
        if old_otp is None:
            return False

        old_otp = json.loads(old_otp)
        old_time = datetime.datetime.strptime(old_otp[1], "%m/%d/%Y, %H:%M:%S")
        if (datetime.datetime.now() - old_time).total_seconds() > 180:
            return False

        if old_otp[0] != login_otp:
            return False

        user.login_otp = None
        user.save()

    return True


def check_permission(request, permissions: list):
    for permission in permissions:
        if not request.user.has_perm(permission):
            raise ValidationError(
                detail={'message': f"You Don't Have Permission for {permission.split('.')[-1]}. Contact Admin."})
    else:
        return True

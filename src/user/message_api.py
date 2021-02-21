from django.conf import settings
import boto3


# AWS Credentials
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION_NAME = settings.AWS_REGION_NAME


def aws_api(phone_no, message):
    # SENDER_ID = ""

    SMS_MOBILE = "+91" + str(phone_no)  # Make sure is set in E.164 format.
    SMS_MESSAGE = message

    # Create an SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    # Send your sms message.
    response = client.publish(
        PhoneNumber=SMS_MOBILE,
        Message=SMS_MESSAGE,
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'String',
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        }
    )

    # print(response)
    # print("MessageId:" + response["MessageId"])
    # print("HTTPStatusCode:" + str(response["ResponseMetadata"]["HTTPStatusCode"]))

    return str(response["ResponseMetadata"]["HTTPStatusCode"])

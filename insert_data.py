import requests
import json
import os
import random

BASE_URL = 'http://127.0.0.1:8000/api/'

os.chdir('src')
os.system("start python manage.py runserver")
while True:
    try:
        response = requests.get(BASE_URL)
        break
    except:
        print("Reconnecting....")
os.chdir('../')


def add_users():
    print(f"{'Adding User ':<25} {': Started':>10}")
    user_data_path = "data/User.json"
    users = json.load(open(user_data_path))
    users_tokens = []
    for user in users:
        response = requests.post(BASE_URL+'user/register/', data=user)
        users_tokens.append(response.json())
    print(f"{'Adding User ':<25} {': Ended':>10}")
    with open("data/users_tokens.json", 'w') as f:
        json.dump(users_tokens, f)


def get_superadmin_token():
    print(f"{'Logging Super User ':<25} {': Started':>10}")
    while True:
        password = input("Enter Superadmin Password : ")
        login_detail = {
            "mobile_no": 1234,
            "password": password
        }

        response = requests.post(BASE_URL+'user/login/', data=login_detail)
        if response.status_code == 200:
            break
    with open("data/super_users_tokens.json", 'w') as f:
        json.dump(response.json(), f)
    print(f"{'Logging Super User ':<25} {': Ended':>10}")


def add_admin_user():
    print(f"{'Adding Admin User ':<25} {': Started':>10}")
    admin_user_path = "data/Admin-User.json"
    admin_users = json.load(open(admin_user_path))
    admins_tokens = []
    super_user_token = json.load(open('data/super_users_tokens.json'))
    headers = {
        'Authorization': 'Bearer {}'.format(super_user_token['access'])
    }
    for admin_user in admin_users:
        response = requests.post(BASE_URL+"user/register/admin/", data=admin_user, headers=headers)
        admins_tokens.append(response.json())
    print(f"{'Adding Admin User ':<25} {': Ended':>10}")
    with open("data/admin_users_tokens.json", 'w') as f:
        json.dump(admins_tokens, f)


def add_product_options():
    print(f"{'Adding Fixtures ':<25} {': Started':>10}")
    os.chdir('src')
    os.system("python manage.py loaddata --app product product_options.json")
    os.chdir("../")
    print(f"{'Adding Fixtures':<25} {': Ended':>10}")


def add_branch_details():
    company_branch_path = "data/Company_Branch.json"
    branch_details = json.load(open(company_branch_path))

    user_token_path = "data/users_tokens.json"
    users_tokens = json.load(open(user_token_path))
    for i, branch_detail in enumerate(branch_details):

        headers = {
            'Authorization': 'Bearer {}'.format(users_tokens[i]['access'])
        }
        response = requests.post(BASE_URL+'user/dummybranchdetyails/', data=branch_detail, headers=headers)
        print(response.status_code, ":: RESPONSE ::", response.json())


def add_company_type():
    print(f"{'Adding Company Type ':<25} {': Started':>10}")
    compay_type_path = "data/Company_Type.json"
    compay_type_details = json.load(open(compay_type_path))

    user_token_path = "data/users_tokens.json"
    users_tokens = json.load(open(user_token_path))
    headers = {
        'Authorization': 'Bearer {}'.format(users_tokens[0]['access'])
    }
    for company_branch_detail in compay_type_details:
        response = requests.post(BASE_URL+'user/details/companytype/', data=company_branch_detail, headers=headers)
    print(f"{'Adding Company Types ':<25} {': Ended':>10}")


def add_product():
    user_data_path = "data/Product.json"
    products = json.load(open(user_data_path))

    user_token_path = "data/users_tokens.json"
    users_tokens = json.load(open(user_token_path))
    print(users_tokens[0]['access'])

    for users_token in range(len(users_tokens)):
        headers = {
            'Authorization': 'Bearer {}'.format(users_tokens[users_token]['access'])
        }
        for product in products:
            response = requests.post(BASE_URL+'product/', data=product, headers=headers)
            print(response.status_code, ":: RESPONSE ::", response.json())


def add_bidrate():
    bid_rate_path = "data/Bid_Rate.json"
    bid_rates = json.load(open(bid_rate_path))

    user_token_path = "data/users_tokens.json"
    users_tokens = json.load(open(user_token_path))

    for users_token in range(len(users_tokens)):
        headers = {
            'Authorization': 'Bearer {}'.format(users_tokens[users_token]['access'])
        }

        for bid_rate in bid_rates:
            response = requests.post(
                BASE_URL + "product/mybid/?p_id={}".format(random.randint(1, 20)),
                data=bid_rate, headers=headers)
            print(response.status_code, ":: RESPONE ::", response.json())


def add_favourite():
    user_token_path = "data/users_tokens.json"
    users_tokens = json.load(open(user_token_path))

    for users_token in range(len(users_tokens)):
        headers = {
            'Authorization': 'Bearer {}'.format(users_tokens[users_token]['access'])
        }
        for i in range(2):
            response = requests.get(
                BASE_URL + "product/favouritesoper/?c_branch={}&status=add".format(random.randint(1, 5)),
                headers=headers)
            print(response.status_code, ":: RESPONE ::", response.json())


def add_state():
    print(f"{'Adding State ':<25} {': Started':>10}")
    state_file = "data/demo-cities.json"
    states = json.load(open(state_file))
    super_user_token = json.load(open('data/super_users_tokens.json'))
    headers = {
        'Authorization': 'Bearer {}'.format(super_user_token['access'])
    }
    for state in states:
        response = requests.post(BASE_URL+'product/state/', data=state, headers=headers)
    print(f"{'Adding State ':<25} {': Ended':>10}")


add_users()
get_superadmin_token()
add_admin_user()
add_company_type()
add_state()
add_product_options()
# add_branch_details()
# add_product()
# add_bidrate()
# add_favourite()

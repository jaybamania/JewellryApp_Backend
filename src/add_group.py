
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
django.setup()


# # }, 'User Setting','User Bid', 'State', 'Payment Option','Delivery Time'


def main():
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Group, Permission
    from user import models as user_models
    from product import models as product_models
    from user.models import (
        User,
        Product
    )

    operation = ['add', 'change', 'delete', 'view']
    change_view = ['change', 'view']

    group_names = {
        'Access Trader’s Listing functionalies': {
            User: ['view'],
            Product: ['add', 'change', 'view'],
        },
        'Aceess to Permit Trader to Add List - All Trader’s Profile Details': {
            user_models.User: change_view,
            user_models.CompanyBranchDetail: change_view,
            user_models.Company: change_view
        },
        'Access all the User’s Bid funcitonality': {
            user_models.User: ['view'],
            product_models.Product: ['view'],
            product_models.BidRate: ['add', 'change', 'view'],
        },
        'States - Regional': {
            product_models.State: ['add', 'change', 'view'],
            product_models.City: ['add', 'change', 'view'],
            product_models.PaymentType: ['add', 'change', 'view'],
            product_models.DeliveryTime: ['add', 'change', 'view'],
        },
        'Relationship State - Product': {
            product_models.State: ['view'],
            product_models.City: ['view'],
            product_models.CommodityForState: ['add', 'change', 'view'],
            product_models.Metal: ['add', 'change', 'view'],
            product_models.MetalCategory: ['add', 'change', 'view'],
            product_models.MetalPurity: ['add', 'change', 'view'],
            product_models.PaymentType: ['add', 'change', 'view'],
            product_models.DeliveryTime: ['add', 'change', 'view'],

        },
    }
    print("started")

    for group_name, perms in group_names.items():
        new_group, created = Group.objects.get_or_create(name=group_name)
        print(new_group)
        for model, perm_lists in perms.items():
            ct = ContentType.objects.get_for_model(model)
            for perm_list in perm_lists:
                print('{}_{}'.format(perm_list, model._meta.model_name))
                permission = Permission.objects.get(codename='{}_{}'.format(perm_list, model._meta.model_name))
                new_group.permissions.add(permission)
        print()
        print("Next Group")


# new_group, created = Group.objects.get_or_create(name='new_group')
# ct = ContentType.objects.get_for_model(Project)
# permission = Permission.objects.create(codename='can_add_project',
#                                        name='Can add project',
#                                        content_type=ct)
# new_group.permissions.add(permission)
if __name__ == "__main__":
    main()

from user.serializers import UserSerializer
from user.models import User
from rest_framework.renderers import JSONRenderer

# TO Save a new User using UserSerializer
data = {
    "name": "Admin 2 Kumar",
    "email": "admin2@gmail.com",
    "password": "admin2"
}

obj = UserSerializer(data=data)

# To see a User data using UserSerializer
u1 = User.objects.first()
obj = UserSerializer(u1)
json = JSONRenderer().render(obj.data)

from forum.models import UserData
from django.contrib.auth import get_user_model

for user in get_user_model().objects.all():
    if len(UserData.objects.filter(user=user)) == 0:
        UserData.objects.create(user=user)
from django.contrib import admin
from django.contrib.auth.models import Group

from account.models import EndUser

admin.site.register(EndUser)

admin.site.unregister(Group)

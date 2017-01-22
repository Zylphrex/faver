from django.contrib import admin
from faver_app.models import FaverUser, FaverRequest, FaverContract

# Register your models here.
admin.site.register(FaverUser)
admin.site.register(FaverRequest)
admin.site.register(FaverContract)

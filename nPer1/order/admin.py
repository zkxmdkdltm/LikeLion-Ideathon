from django.contrib import admin
from .models import Order, Store, Menu, Log

admin.site.register(Order)
admin.site.register(Store)
admin.site.register(Menu)
admin.site.register(Log)

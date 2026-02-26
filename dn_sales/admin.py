from django.contrib import admin
from dn_sales import models


admin.site.register(models.Sale)
admin.site.register(models.SoldProduct)
admin.site.register(models.CashTracker)
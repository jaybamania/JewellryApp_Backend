from django.contrib import admin

from . import models


admin.site.register(models.Product)
admin.site.register(models.Metal)
admin.site.register(models.MetalCategory)
admin.site.register(models.MetalPurity)
admin.site.register(models.CommodityForState)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.DeliveryTime)
admin.site.register(models.PaymentType)
admin.site.register(models.BidRate)
admin.site.register(models.MarketTime)

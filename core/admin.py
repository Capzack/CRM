from django.contrib import admin
from .models import Profile, Lid, Company, Product, Deal, Contact, PorductInDeal


class ProductInline(admin.TabularInline):
    model = PorductInDeal
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)


class DealAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)


admin.site.register(Deal, DealAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register([Profile, Lid, Company, Contact])


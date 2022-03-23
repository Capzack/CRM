from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.defaulttags import url

from .models import Lid, Company, Product, Deal, Contact, PorductInDeal, Sell, Components, ComponentsInProducts


class ProductInline(admin.TabularInline):
    model = PorductInDeal
    extra = 1


class ComponentsInline(admin.TabularInline):
    model = ComponentsInProducts
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)
    inlines = (ComponentsInline,)


class DealAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)


class ComponentsAdmin(admin.ModelAdmin):
    inlines = (ComponentsInline,)


admin.site.register(Deal, DealAdmin)
admin.site.register(Components, ComponentsAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register([Lid, Company, Contact, Sell])


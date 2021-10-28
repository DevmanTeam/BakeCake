from django.contrib import admin


from .models import Cake, Order


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('cost',)
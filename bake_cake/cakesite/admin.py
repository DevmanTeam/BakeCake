from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Cake, Order


class OrderResource(resources.ModelResource):

    class Meta:
        model = Order


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    readonly_fields = ('cost',)
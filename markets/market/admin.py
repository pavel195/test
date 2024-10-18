from django.contrib import admin
from .models import Market, Unit, MarketUnitPriority


class MarketAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


class MarketUnitPriorityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Market, MarketAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(MarketUnitPriority, MarketUnitPriorityAdmin)

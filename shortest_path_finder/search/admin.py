from django.contrib import admin
from .models import Distance, District

# Register your models here.

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_parent_districts')
    
    def get_parent_districts(self, obj):
        return ", ".join([parent.name for parent in obj.parent_districts.all()])
    
    get_parent_districts.short_description = 'Parent Districts'
    
admin.site.register(District, DistrictAdmin)
admin.site.register(Distance)

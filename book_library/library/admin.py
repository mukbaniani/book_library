from django.contrib import admin
from  .models import Branch,Book,Order

admin.site.index_title = 'ბიბლიოთეკარი'
admin.site.site_header = 'ცოდვილების ჩათის ბიბლიოთეკა'
admin.site.site_title = 'სამართავი პანელი'

@admin.register(Book)
class BookAdminArea(admin.ModelAdmin):
    list_display = ('name', 'author', 'quantity')
    list_display_links = ['name']
    list_filter = ('author',)
    list_per_page = 10
    search_fields = ['name', 'author']

@admin.register(Order)
class OrderAdminArea(admin.ModelAdmin):
    search_fields = ('start_date', 'end_date')
    list_per_page = 10

admin.site.register(Branch)
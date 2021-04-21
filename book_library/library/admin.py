from django.contrib import admin
from  .models import Branch, Book, Order
import datetime

admin.site.index_title = 'ბიბლიოთეკარი'
admin.site.site_header = 'ცოდვილების ჩათის ბიბლიოთეკა'
admin.site.site_title = 'სამართავი პანელი'

@admin.register(Branch)
class BranchAdminArea(admin.ModelAdmin):
    search_fields = ['work_day']
    list_per_page = 10
    list_display = ['address', 'work_day', 'tel_number']
    list_editable = ['work_day', 'tel_number']


@admin.register(Book)
class BookAdminArea(admin.ModelAdmin):
    search_fields = ('name', 'author')
    list_per_page = 10
    list_display = ('author', 'name', 'quantity')
    list_display_links = ['author']
    list_editable = ['name', 'quantity']
    autocomplete_fields = ['branch']
    list_filter = ('author',)
    

@admin.register(Order)
class OrderAdminArea(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name')
    list_per_page = 10
    list_display = ('user', 'start_date', 'end_date', 'count_return_date', 'status')
    list_display_links = ('user', 'start_date')
    list_editable = ['end_date', 'status']
    autocomplete_fields = ['book', 'user', 'branch']
    list_filter = ['status']

    def count_return_date(self, obj):
        count_date = (obj.end_date - datetime.date.today()).days
        if count_date < 0 and obj.status is False:
            return 'დააგვიანა'
        elif obj.status is True:
            return 'დაბრუნებულია'
        return f'{count_date} დღე'
    count_return_date.short_description = 'დაბრუნებდამდე დარჩა'

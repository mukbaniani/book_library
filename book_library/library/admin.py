from django.contrib import admin
from  .models import Branch, Book, Order,History, Todo, Quantity
import datetime
from django.db.models import F

admin.site.index_title = 'ბიბლიოთეკარი'
admin.site.site_header = 'ცოდვილების ჩათის ბიბლიოთეკა'
admin.site.site_title = 'სამართავი პანელი'


class InlineQuantity(admin.StackedInline):
    model = Quantity


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
    inlines = [InlineQuantity]
    list_display = ('author', 'name')
    list_display_links = ['author']
    list_editable = ['name']
    list_filter = ('author',)
    

@admin.register(Order)
class OrderAdminArea(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name')
    list_per_page = 10
    list_display = ('user', 'start_date', 'end_date', 'count_return_date', 'status')
    list_display_links = ('user', 'start_date')
    autocomplete_fields = ['book']
    list_filter = ['status']

    def count_return_date(self, obj):
        count_date = (obj.end_date - datetime.date.today()).days
        if count_date < 0 and obj.status is False:
            return 'დააგვიანა'
        elif obj.status is True:
            return 'დააბრუნა'
        return f'{count_date} დღე'
    count_return_date.short_description = 'დაბრუნებდამდე დარჩა'


@admin.register(History)
class HistoryAdminArea(admin.ModelAdmin):
    list_filter = ('return_book__branch',)


admin.site.register([Todo, Quantity])
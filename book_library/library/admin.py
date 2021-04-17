from django.contrib import admin
from  .models import Branch,Book,Order

admin.site.register([Branch,Book,Order])
# Register your models here.

from django.contrib import admin
from rango.models import Category, Page

# Create model admin class to pass to register. 
# This changes he admin options for the app
class PageAdmin(admin.ModelAdmin):

    # List display admin option (tuple of field names to display on the list page for the object)
    list_display = ('title','category','url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
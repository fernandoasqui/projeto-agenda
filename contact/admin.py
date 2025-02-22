from django.contrib import admin
from contact.models import Contact, Category


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'show', 'email', 'phone',)
    ordering = '-id',
    search_fields = ('first_name', 'last_name', 'email', 'phone',)
    list_per_page = 10
    list_max_show_all = 100
    list_editable = 'first_name', 'last_name', 'show',
    list_display_links = 'id', 'phone',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

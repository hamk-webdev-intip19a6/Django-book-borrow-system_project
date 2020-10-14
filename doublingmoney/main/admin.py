from django.contrib import admin

from .models import Book, Review, Author, Inventory, Rental

class BookAdmin(admin.ModelAdmin):
   
    fieldsets = [
        (None,               {'fields': ['title', 'description', 'image']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Author information',{'fields': ['author']})
    ]
    list_display = ('title', 'pub_date')

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'available')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'inventory', 'rental_date', 'expire_date', 'book_returned', 'return_date')
    list_filter = ['expire_date', 'user']
    search_fields = ['user__username']

admin.site.register(Book, BookAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Review)
admin.site.register(Rental, RentalAdmin)
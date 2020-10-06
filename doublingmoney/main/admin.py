from django.contrib import admin

from .models import Book, Review, Author, Inventory, Rental, Payment

class BookAdmin(admin.ModelAdmin):
    fields = [
        'title', 'description', 'pub_date', 'image', 'rental_rate', 
        'replacement_cost', 'author'
    ]

    list_display = ('title', 'pub_date')

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'available')

class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name']
    
admin.site.register(Book, BookAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Rental)
admin.site.register(Payment)


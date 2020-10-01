from django.contrib import admin

from .models import Book, Book_author, Review, Author, Inventory

class BookAuthorInLine(admin.StackedInline):
    model = Book_author
    extra = 1

class BookAdmin(admin.ModelAdmin):
    fields = [
        'title', 'description', 'pub_date', 'image', 'rental_rate', 
        'replacement_cost'
    ]
    inlines = [BookAuthorInLine]
    list_display = ('title', 'pub_date')

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'available')


admin.site.register(Book, BookAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Book_author)


from django.contrib import admin
from .models import Book, Book_author, Review, Author

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Book_author)
admin.site.register(Review)
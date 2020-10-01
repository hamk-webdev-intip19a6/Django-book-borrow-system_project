from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import generic
from django.db.models import Count

from .models import Book, Book_author, Inventory, Author

class HomeView(generic.ListView):
    template_name = 'main/home.html'
    context_object_name = "available_book_list"

    def get_queryset(self):
        """returns list of available books. 
        IF many of the same book add copies count"""

        q1 = Book.objects.filter(inventory__available=True)
        q1 = q1.annotate(copies=Count('title'))
        return q1
"""
def home(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'main/home.html', context)
"""
def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
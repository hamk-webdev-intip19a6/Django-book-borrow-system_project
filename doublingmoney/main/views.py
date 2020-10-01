from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
#from django.views import generic
from django.views.generic import (
    ListView,
    #DetailView,
    #CreateView,
    #UpdateView,
    #DeleteView
)
from django.db.models import Count, Q

from .models import Book, Book_author, Inventory, Author


class HomeView(ListView):
    template_name = 'main/home.html'
    context_object_name = "available_book_list"

    def get_queryset(self):
        # returns list of available books.IF many of the same book add copies count
        q = Book.objects.filter(inventory__available=True)
        q = q.annotate(copies=Count('title'))
        return q

class SearchResultView(ListView):
    model = Book
    template_name = 'main/search_results.html'
    context_object_name = "book_list"

    def get_queryset(self):
        query = self.request.GET.get('q')
        book_list = Book.objects.filter(
            Q(title__icontains=query) 
            | Q(book_author__author_id__first_name__icontains=query)
            | Q(book_author__author_id__last_name__icontains=query)
        ).distinct()
        return book_list

def book(request, book):
    book = book
    book_title = Book.objects.filter(title = book)
    available = Book.objects.filter(inventory__available=True, title=book).annotate(copies=Count('title'))
    authors = Author.objects.filter(book_author__book_id__title = book)
    context = {'book_title': book_title, 
                'available': available, 
                'authors': authors}
                
    return render(request, 'main/book.html', context)

def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
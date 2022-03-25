from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
import datetime
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
    # UpdateView,
    # DeleteView
)
from django.db.models import Count, Q, OuterRef, Subquery, Value, When, Case, Avg, Max, Min, Sum
from django.db.models.functions import Concat
from .models import Book, Inventory, Author, Rental, Review
from star_ratings.models import Rating
from .forms import RentForm, CommentForm

class HomeView(ListView):
    model = Book
    template_name = 'main/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rate'
    def get_queryset(self):
        q = Book.objects.filter(inventory__available=True).filter(ratings__isnull=False).annotate(copies=Count('title')).order_by('-ratings__average')[:6]
        return q

class BooksListing(ListView):
    template_name = 'main/books.html'
    context_object_name = "available_book_list"
    model = Book
    ordering = ['-date_posted']
    paginate_by = 6
    def get_queryset(self):
        # returns list of available books.IF many of the same book add copies count
        q = Book.objects.filter(inventory__available=True).annotate(copies=Count('title'))
        return q

class SearchResultView(ListView):
    template_name = 'main/search_results.html'
    context_object_name = "book_list"
    model = Book
    ordering = ['-date_posted']
    paginate_by = 6
    def get_queryset(self):
        query = self.request.GET.get('q')
        book_list = Book.objects.filter(
                inventory__available__isnull=False).annotate(
                    available=Count(
                        Case( When(inventory__available=True, then=Value(1)) )
                )
            )
        if query:
            # | Q(book_author__author_id__first_name__icontains=query)
            # | Q(book_author__author_id__last_name__icontains=query)
            book_list = book_list.filter(title__icontains=query)
        return book_list

class BookView(DetailView, CreateView):
    template_name = 'main/book.html'
    context_object_name = "book"
    model = Book

    form_class = CommentForm

    def get_success_url(self):
        b = self.kwargs['pk']
        return reverse('main:main-book', kwargs={ 'pk': b } )

    def form_valid(self, form):
        b = self.kwargs['pk']
        form.instance.user = self.request.user
        comment = form.cleaned_data.get('comment')
        form.instance.book_id = b
        form.instance.review = comment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        b = self.kwargs['pk']
        context['comments'] = Review.objects.filter( book=b )
        return context

    def get_queryset(self):
        q = Book.objects.filter(inventory__available__isnull=False).annotate(copies=Count(Case(When(inventory__available=True, then=Value(1) ) ) ) )
        return q

@login_required
def rent(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    inventory = Inventory.objects.filter(available=True, book__id=book_id).first()

    if request.method == 'POST':
        form = RentForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.instance.inventory = inventory
            form.instance.expire_date = timezone.now() + datetime.timedelta(weeks=int(form.cleaned_data['duration']))
            inventory.available = False
            inventory.save()
            form.save()
        return HttpResponseRedirect(reverse('profile'))
    else:
        form = RentForm(initial={'duration': '2'})
    context = {
        'form': form,
        'book': book}

    return render(request, 'main/rent.html', context)

def returnBook(request, rental_id):
    Inventory.objects.filter(rental__id=rental_id).update(available=True)
    Rental.objects.filter(pk=rental_id).update(book_returned=True, return_date=timezone.now())
    messages.success(request, f'Book has been returned succesfully')
    return HttpResponseRedirect(reverse('profile'))
    
def returnSuccess(request):
    messages.success(request, f'Book has been returned succesfully')
    return HttpResponseRedirect(reverse('profile'))

'''
def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
'''

# HTTP Error 404
def page_not_found(request, exception):
        response = render(request, "main/errors/404.html", {} )
        response.status_code = 404
        return response
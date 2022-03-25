from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.HomeView.as_view(), name='main-home'),
    path('books/', views.BooksListing.as_view(), name='main-books'),
    path('<int:pk>/', views.BookView.as_view(), name='main-book'),
    path('search/', views.SearchResultView.as_view(), name='search_results'),
    path('<book_id>/rent/', views.rent, name='rent'),
    path('profile/return/<rental_id>/', views.returnBook, name='returnBook'),
    path('profile/return/returnSuccess/', views.returnSuccess, name="returnSuccess"),
    #path('about/', views.about, name='main-about'),
]
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.urls import reverse

class Book(models.Model):
    name = models.CharField(max_length=64)
    author = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    copies = models.IntegerField(default=0)
    image = models.ImageField(default='default_book.jpg', upload_to='book_pics')
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'Book name: {self.name}, Author: {self.author}'

class Review(models.Model):
    review = models.CharField(max_length=512)
    stars = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} Reviews'

class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
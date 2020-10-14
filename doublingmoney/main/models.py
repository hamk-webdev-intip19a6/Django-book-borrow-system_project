from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    class Meta:
        unique_together = ["first_name", "last_name"]
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.ManyToManyField(Author)
    description = models.CharField(max_length=128)
    pub_date = models.DateField('date published')
    image = models.ImageField(default='default_book.jpg', upload_to='book_pics')
    last_update = models.DateTimeField(default=timezone.now)
    ratings = GenericRelation(Rating, related_query_name='books')
    def __str__(self):
        return f'{self.title}'

class Inventory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    available = models.BooleanField('Available', default=True)
    
    def __str__(self):
        return f'{self.book}'

class Rental(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(default=timezone.now)
    book_returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.inventory} {self.rental_date} {self.expire_date}'

class Review(models.Model):
    review = models.CharField(max_length=512)
    date = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Reviews'
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.urls import reverse

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
    rental_rate = models.DecimalField(default=4.99, max_digits=4, decimal_places=2)
    replacement_cost = models.DecimalField(default=29.99, max_digits=5, decimal_places=2)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'

class Inventory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    available = models.BooleanField('Available', default=False)
    
    def __str__(self):
        return f'{self.book}'

class Rental(models.Model):
    inventory = models.OneToOneField(Inventory, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.inventory} {self.rental_date} {self.expire_date}'

class Payment(models.Model):
    user =  models.ForeignKey(User, on_delete=models.RESTRICT)
    rental = models.ForeignKey(Rental, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    method = models.CharField(max_length=32)
    payment_date = models.DateTimeField(default=timezone.now)

class Review(models.Model):
    review = models.CharField(max_length=512)
    stars = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Reviews'

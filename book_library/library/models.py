from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Branch(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Book(models.Model):
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    book=models.ManyToManyField(Book)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()

    def __str__(self):
        return self.book.name



from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import datetime

User = get_user_model()


class Branch(models.Model):
    address=models.CharField(
        max_length=100,
        verbose_name=_('მისამართი'))
    work_day = models.CharField(
        max_length=40,
        verbose_name=_('სამუშაო დღეები')
    )
    tel_number = models.CharField(
        max_length=40,
        verbose_name=_('ტელეფონის ნომერი')
    )

    def __str__(self):
        return self.address


    class Meta:
        verbose_name = 'ფილიალები'
        ordering = ['-id']


class Book(models.Model):
    name=models.CharField(max_length=100, verbose_name=_('წიგნის სახელი'))
    author=models.CharField(max_length=100, verbose_name=_('ავტორი'))
    quantity=models.IntegerField(default=0, verbose_name=_('მარაგი'))
    branch = models.ManyToManyField(Branch, verbose_name=_('ფილიალი'))
    Condition=models.IntegerField(default=10,verbose_name=_('წიგნის მდოგმარეობა'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'წიგნები'
        ordering = ['-id']


class Order(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('წიგნი'))
    user=models.ForeignKey(User,on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE, verbose_name=_('ფილიალი'))
    start_date=models.DateField(verbose_name=_('შეკვეთის დრო'))
    end_date=models.DateField(verbose_name=_('დაბრუნების დრო'), blank=True, null=True)
    status = models.BooleanField(verbose_name=_('სტატუსი'), default=False)

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        today = datetime.datetime.now()
        if not self.pk:
            self.book.quantity-=1
            self.book.save()
            self.end_date = today + datetime.timedelta(days=14)
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'შეკვეთები'
        ordering = ['-id']

class History(models.Model):
    return_time=models.BooleanField(verbose_name=_('დააბრუნა მის დროზე?'))
    return_book=models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name=_('რომელი წიგნი დააბრუნა'))
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name=_('მომხმარებელი'))
    condition=models.IntegerField(default=10,verbose_name=_('წიგნის მდოგმარეობა'))

    def __str__(self):
        return self.return_book

    def save(self,*args,**kwargs):
        if not self.pk:

            self.return_book.Condition = self.condition
            self.return_book.save()
        super(History,self).save(*args,**kwargs)

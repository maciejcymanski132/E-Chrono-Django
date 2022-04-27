from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    Title = models.CharField(max_length=50)


class Author(models.Model):
    Firstname = models.CharField(max_length=30, blank=False)
    Lastname = models.CharField(max_length=30, blank=False)


class Provider(models.Model):
    Name = models.CharField(max_length=50, blank=False)
    Phone_number = PhoneNumberField(null=False, blank=False, unique=True)


class Book(models.Model):
    Provider = models.ForeignKey(Provider,on_delete=models.CASCADE)
    Title = models.CharField(max_length=200)
    Pub_Date = models.DateTimeField('date published')
    Author = models.ForeignKey(Author,on_delete=models.DO_NOTHING)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Available = models.BooleanField()

    def __str__(self):
        return f"Book provided by:{Provider.Name}\n" \
               f"Title:{Title}" \
               f"Publication date {Pub_Date}" \
               f"Author:{Author.Firstname} + {Author.Lastname}"



class RentHistory(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    rent_date = models.DateTimeField()
    return_date = models.DateTimeField()


class Customer(models.Model):
    Firstname = models.CharField(max_length=30, blank=False)
    Lastname = models.CharField(max_length=30, blank=False)
    History = models.OneToOneField(RentHistory, on_delete=models.CASCADE)



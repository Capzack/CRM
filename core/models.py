from django.db import models
from django.contrib.auth.models import User

roles = {
    ('seller', 'seller')
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=roles)


class Lid(models.Model):
    Name = models.CharField(max_length=50)
    Emale = models.CharField(max_length=50)
    Phone = models.CharField(max_length=50)
    Company = models.ForeignKey("Company", on_delete = models.CASCADE)
    Interes = models.ForeignKey("Product", on_delete = models.CASCADE)

    def __str__(self):
        return self.Name


class Company(models.Model):
    Area = models.CharField(max_length=50)
    Number_of_worker = models.CharField(max_length=50)
    Emale = models.CharField(max_length=50)
    Phone = models.CharField(max_length=50)
    Site = models.CharField(max_length=50)
    Banque = models.CharField(max_length=50)

    def __str__(self):
        return self.Area


class Deal(models.Model):
    Sum = models.IntegerField(default=0)
    Customer = models.ForeignKey("Contact", on_delete=models.CASCADE)
    Commentary = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        print("deal")
        super(Deal, self).save(*args, **kwargs)
        self.Sum = self.calculate_sum()
        super(Deal, self).save(*args, **kwargs)

    def calculate_sum(self):
        return sum(x[0] for x in list(PorductInDeal.objects.filter(Deal=self).values_list('sum')))


class Product(models.Model):
    Name = models.CharField(max_length=50)
    Price = models.IntegerField()

    def __str__(self):
        return self.Name

    def get_price(self):
        return self.Price


class PorductInDeal(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    sum = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        print(*args, **kwargs)
        print("Prod")
        self.sum = self.calculate_sum()
        super(PorductInDeal, self).save(*args, **kwargs)
        self.Deal.save()

    def calculate_sum(self):
        return self.Product.Price * self.count


class Contact(models.Model):
    Name = models.CharField(max_length=50)
    Emale = models.CharField(max_length=50)
    Phone = models.CharField(max_length=50)
    Company = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.Name



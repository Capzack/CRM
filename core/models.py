from django.db import models
from django.contrib.auth.models import User

Channel = {
    ('site', 'Сайт'), ('phone', 'Телефон'), ('social', 'Социальные сети'), ('email', 'Електронная почта')
}
Status ={
    ('New', 'Новый'), ('Kvali', 'Квалификация'), ('Defeat', 'Проигрышный статус'), ('Deal', 'В сделке'), ('Sell', 'В продаже')
}

DealStatus ={
    ('New', 'Новый'), ('Interes', 'Выяснение интереса'), ('Chek', 'Проверка закупки '), ('Offer', 'Rоммерческое предложение'), ('Done', 'Завершенна')
}

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)


class Lid(models.Model):
    Name = models.CharField(max_length=50, verbose_name='Имя')
    Emale = models.CharField(max_length=50, verbose_name='Почта')
    Phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    Company = models.ForeignKey("Company", on_delete=models.CASCADE, verbose_name='Компания')
    Interes = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name='Первичный интерес')
    Channel = models.CharField(max_length=30, choices=Channel, verbose_name='Канал обращения')
    Manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Ответсвенный сотрудник')
    Status = models.CharField(max_length=30, choices=Status, verbose_name='Стадия')
    def __str__(self):
        return self.Name
    class Meta:
        verbose_name = 'Лиды'
        verbose_name_plural = 'Лиды'


class Company(models.Model):
    Area = models.CharField(max_length=50, verbose_name='Сфера')
    Number_of_worker = models.CharField(max_length=50, verbose_name='Число сотрудников')
    Emale = models.CharField(max_length=50, verbose_name='Почта')
    Phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    Site = models.CharField(max_length=50, verbose_name='Сайт компании')
    Banque = models.CharField(max_length=50, verbose_name='Реквизиты')

    def __str__(self):
        return self.Area

    class Meta:
        verbose_name = 'Компании'
        verbose_name_plural = 'Компании'

class Deal(models.Model):
    Sum = models.IntegerField(default=0, verbose_name='Сумма')
    Customer = models.ForeignKey("Contact", on_delete=models.CASCADE, verbose_name='Покупатель')
    Commentary = models.CharField(max_length=500, verbose_name='Комментарий')
    Manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Ответсвенное лицо')
    Status = models.CharField(max_length=30, choices=DealStatus, verbose_name='Стадия')
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        print("deal")
        super(Deal, self).save(*args, **kwargs)
        self.Sum = self.calculate_sum()
        super(Deal, self).save(*args, **kwargs)

    def calculate_sum(self):
        return sum(x[0] for x in list(PorductInDeal.objects.filter(Deal=self).values_list('sum')))
    class Meta:
        verbose_name = 'Сделки'
        verbose_name_plural = 'Сделки'


class Sell(models.Model):
    Deal = models.ForeignKey("Deal", on_delete=models.CASCADE, verbose_name='Сделка')
    Manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Ответсвенное лицо')
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = 'Продажи'
        verbose_name_plural = 'Продажи'


class Product(models.Model):
    Name = models.CharField(max_length=50, verbose_name='Наименование')
    Price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.Name

    def get_price(self):
        return self.Price

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


class Components(models.Model):
    Name = models.CharField(max_length=50, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Составляющие'
        verbose_name_plural = 'Составляющие'
    def __str__(self):
        return self.Name

class ComponentsInProducts(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    Components = models.ForeignKey(Components, on_delete=models.CASCADE, verbose_name='Компонент')
    count = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компонент'

    def __str__(self):
        return "Компонент"

class PorductInDeal(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    Deal = models.ForeignKey(Deal, on_delete=models.CASCADE, verbose_name='Сделка')
    count = models.IntegerField(default=1, verbose_name='Количество')
    sum = models.IntegerField(default=0, verbose_name='Сумма')

    def save(self, *args, **kwargs):
        self.sum = self.calculate_sum()
        super(PorductInDeal, self).save(*args, **kwargs)
        self.Deal.save()

    def calculate_sum(self):
        return self.Product.Price * self.count

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return 'Товары'


class Contact(models.Model):
    Name = models.CharField(max_length=50, verbose_name='Имя')
    Emale = models.CharField(max_length=50, verbose_name='Почта')
    Phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    Company = models.ForeignKey("Company", on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


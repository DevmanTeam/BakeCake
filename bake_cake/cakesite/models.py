from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("Заявка обрабатывается", "заявка обрабатывается"),
        ("Готовим ваш торт", "готовим ваш торт"),
        ("Торт в пути", "торт в пути"),
        ("Торт у вас", "торт у вас")
    ]

    comment = models.TextField('Комментарий к заказу',
                               max_length=200,
                               blank=True,
                               null=True)
    address = models.CharField('Адрес доставки', max_length=100)
    delivery_date = models.DateTimeField("Дата доставки", blank=True, null=True,
                                     db_index=True)
    order_status = models.CharField("Статус заказа", max_length=30,
                                    choices=ORDER_STATUS_CHOICES,
                                    default="Необработанный",
                                    db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders',
                             verbose_name='пользователь')
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return self.address


class Cake(models.Model):

    LEVELS_COUNT_CHOICES = [
        ("1", "1 уровень"),
        ("2", "2 уровня"),
        ("3", "3 уровня"),
    ]

    CAKE_FORM_CHOICES = [
        ("Квадрат", "квадрат"),
        ("Круг", "круг"),
        ("Прямоугольник", "прямоугольник"),
    ]

    TOPPING_CHOICES = [
        ("Без топпинга", "без топпинга"),
        ("Белый соус", "белый соус"),
        ("Карамельный сироп", "карамельный сироп"),
        ("Кленовый сироп", "кленовый сироп"),
        ("Клубничный сироп", "клубничный сироп"),
        ("Черничный сироп", "черничный сироп"),
        ("Молочный шоколад", "молочный шоколад"),
    ]

    BERRIES_CHOICES = [
        ("Ежевика", "ежевика"),
        ("Малина", "малина"),
        ("Голубика", "голубика"),
        ("Клубника", "клубника"),
    ]

    DECOR_CHOICES = [
        ("Фисташки", "фисташки"),
        ("Безе", "безе"),
        ("Фундук", "фундук"),
        ("Пекан", "пекан"),
        ("Маршмеллоу", "маршмеллоу"),
        ("Марципан", "марципан"),
    ]

    levels_count = models.CharField('количество уровней',
                                    max_length=50,
                                    choices=LEVELS_COUNT_CHOICES,
                                    db_index=True)
    cake_form = models.CharField('форма торта',
                                 max_length=50,
                                 choices=CAKE_FORM_CHOICES,
                                 db_index=True
                                 )
    topping = models.CharField('топпинг',
                               max_length=50,
                               choices=CAKE_FORM_CHOICES,
                               db_index=True
                               )
    berries = models.CharField('ягоды',
                               max_length=50,
                               choices=BERRIES_CHOICES,
                               db_index=True, blank=True,
                               null=True,
                               )
    decor = models.CharField('декор',
                             max_length=50,
                             choices=DECOR_CHOICES,
                             db_index=True, blank=True,
                             null=True,
                             )
    inscription = models.CharField('надпись', max_length=50, blank=True,
                                   null=True
                                   )
    promocode = models.CharField('промокод',
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 )
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='cakes',
                              verbose_name='торт')

    class Meta:
        verbose_name = 'торт'
        verbose_name_plural = 'торты'



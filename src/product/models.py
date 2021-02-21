from django.db import models


TRADE = [('SELL', "Sell"), ("BUY", "Buy")]
PREMIUM_TYPE = [('+ve', '+ve'), ("-ve", "-ve")]


class Product(models.Model):
    """ For storing detail about a Product(Bullion) and the Seller who has added it """

    quantity = models.IntegerField()
    premium_value = models.FloatField()  # for profit margin price
    premium_type = models.CharField(max_length=5, choices=PREMIUM_TYPE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    trade = models.CharField(max_length=5, choices=TRADE)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name="Product_fk_User",
    )
    metal = models.ForeignKey(
        'Metal',
        on_delete=models.PROTECT
    )
    metal_category = models.ForeignKey(
        'MetalCategory',
        on_delete=models.PROTECT
    )
    metal_purity = models.ForeignKey(
        'MetalPurity',
        on_delete=models.PROTECT,
    )
    delivery_time = models.ForeignKey(
        "DeliveryTime",
        on_delete=models.PROTECT,
    )
    payment_type = models.ForeignKey(
        'PaymentType',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return "{} {} {} {}".format(self.trade, self.metal.name, self.metal_category.name, self.metal_purity.name)

    def __repr__(self):
        return "{} {} {} {}".format(self.trade, self.metal.name, self.metal_category.name, self.metal_purity.name)


class PaymentType(models.Model):
    """ For storing (Bank, Cash) """
    payment_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.payment_type

    def __repr__(self):
        return self.payment_type


class DeliveryTime(models.Model):
    """ For storing (T+1), (T+2) """
    time = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.time

    def __repr__(self):
        return self.time


class City(models.Model):
    "List Of Cities Where App can Work"
    city_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.city_name

    def __repr__(self):
        return self.city_name


class State(models.Model):
    "List Of States Where App can Work"
    state_name = models.CharField(max_length=128, unique=True)
    city = models.ManyToManyField('City')

    def __str__(self):
        return self.state_name

    def __repr__(self):
        return self.state_name


class CommodityForState(models.Model):
    """ For storing relationship between metal, metal_category, metal_purity """
    state_id = models.ForeignKey("State", on_delete=models.PROTECT)
    metal = models.ForeignKey("Metal", on_delete=models.PROTECT)
    metal_category = models.ForeignKey("MetalCategory", on_delete=models.PROTECT)
    metal_purity = models.ManyToManyField('MetalPurity')
    is_active = models.BooleanField(default=False)

    class Meta():
        constraints = [
            models.UniqueConstraint(fields=["state_id", "metal", "metal_category"], name="all_keys_unique_together")
        ]

    def __str__(self):
        return f'{self.state_id.state_name} - {self.metal.name}'

    def __repr__(self):
        return f'{self.state_id.state_name} - {self.metal.name}'


class Metal(models.Model):
    """ For Storing (Gold, Silver) """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MetalCategory(models.Model):
    """ For Storing (Coin, Bar) """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MetalPurity(models.Model):
    """ For Storing (999, 995) """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class BidRate(models.Model):
    """ For biding of the product """

    bid_user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    bid_product = models.ForeignKey('Product', on_delete=models.CASCADE)
    bid_price = models.FloatField(default=None)
    is_notified = models.BooleanField(default=False)


class MarketTime(models.Model):
    """ For Market Watch Time"""

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.start_time + self.end_time

    def __repr__(self):
        return self.start_time + self.end_time

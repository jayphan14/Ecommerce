from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import AutoField, CharField, IntegerField
from django.db.models.fields.related import ForeignKey

class User(AbstractUser):
    pass



class Bid(models.Model):   
    id = models.AutoField(primary_key=True)
    value = IntegerField()
    def __str__(self) -> str:
        return f"{self.id} : {self.value}, by {self.bidder}"

class Category(models.Model):
    category = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"category : {self.category}"



class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    item = CharField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = ForeignKey(User,on_delete=models.CASCADE, related_name="user")
    category = ForeignKey(Category, on_delete=models.CASCADE)
    url = CharField(max_length = 1000)
    description = CharField(max_length = 1000)
    avai = models.BooleanField()
    bidder = ForeignKey(User,on_delete=models.CASCADE, related_name="bidder", null=True)
    def __str__(self) -> str:
        return f"Starting price {self.price} by {self.user}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = CharField(max_length=1000)
    commenter = ForeignKey(User, on_delete=models.CASCADE)
    item = ForeignKey(Listing,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.comment} by {self.commenter}"
    
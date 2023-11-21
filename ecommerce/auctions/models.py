from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django.db import models
from django.conf import settings
from django.template.defaultfilters import date


class Category(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category}"


class Auction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auction_user")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    picture = models.URLField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.CASCADE, related_name="auction_category")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, created by: {self.user} on {date(self.date, 'SHORT_DATETIME_FORMAT')}."


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        # fields = ["title", "description", "category", "picture", "price"]
        exclude = ["user", "date"]

    def save(self, user):
        object = super().save(commit=False)
        object.user = user
        object.save()
        return object


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        Auction, blank=True, related_name="user_watchlist")


class Bids(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="bid_auction")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_user")
    bid = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "date"

    def __str__(self):
        return f"{self.bid}"


class BidsForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["bid"]

    def save(self, user, auction):
        object = super().save(commit=False)
        object.user = user
        object.auction = auction
        object.save()
        return object


class Comments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="comment_auction")

    def __str__(self):
        return f"{date(self.date, 'SHORT_DATETIME_FORMAT')} User: {self.user} commented: {self.comment}"


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]

    def save(self, user, auction):
        object = super().save(commit=False)
        object.user = user
        object.auction = auction
        object.save()
        return object

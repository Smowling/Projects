from django.contrib import admin
from .models import User, Category, Auction, Bids, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bids)
admin.site.register(Comments)

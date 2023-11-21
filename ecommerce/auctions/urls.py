from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing", views.listing, name="listing"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

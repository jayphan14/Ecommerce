from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listing", views.listing, name="listing"),
    path("item/<int:id>", views.display, name="display"),
    path("item/watchlist", views.watchlist, name = "watchlist"),
    path("item/bid", views.bid, name="bid"),
    path("item/close", views.close, name="close"),
    path("item/comment", views.comment, name="comment"),
    path("sold", views.sold, name="sold"),
    path("category", views.category, name="category")
]

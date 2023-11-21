from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Auction, AuctionForm, Bids, Comments, CommentsForm


def index(request):
    auctions = Auction.objects.all()
    for auction in auctions:
        try:
            bid = Bids.objects.all().filter(auction=auction).latest()
            auction.price = bid.bid
        except:
            pass

    return render(request, "auctions/index.html", {"auctions": auctions})


def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {"categories": categories})


def category_listings(request, category):
    cat = Category.objects.get(category=category)
    auctions = Auction.objects.all().filter(category=cat)
    for auction in auctions:
        try:
            bid = Bids.objects.all().filter(auction=auction).latest()
            auction.price = bid.bid
        except:
            pass

    return render(request, "auctions/category_listings.html",
                  {"title": category,
                   "auctions": auctions})


@login_required
def watchlist(request):
    u = User.objects.get(id=request.user.id)
    auctions = u.watchlist.all()
    return render(request, "auctions/watchlist.html", {"auctions": auctions})


@login_required
def listing(request):
    if request.method == "GET":
        return render(request, "auctions/listing.html", {"form": AuctionForm()})

    # POST
    form = AuctionForm(request.POST)
    if not form.is_valid():
        return render(request, "auctions/listing.html", {"form": form})

    # all good, save redirect
    auction = form.save(request.user)
    return HttpResponseRedirect(reverse("auction", args=[auction.id]))


def auction(request, auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
    except:
        raise Http404("Auction doesn't exists.")

    try:
        highest_bid = Bids.objects.all().filter(auction=auction).latest()
    except:
        highest_bid = auction.price

    comments = Comments.objects.order_by("-date").all().filter(auction=auction)

    if request.user.id is not None:
        u = User.objects.get(id=request.user.id)
        if u.watchlist.all().filter(id=auction.id):
            watching = True
        else:
            watching = False
    else:
        watching = False

    if request.method == "POST" and "comment" in request.POST:
        new_comment = CommentsForm(request.POST)
        if not new_comment.is_valid():
            return render(request, "auctions/auction.html",
                          {"auction": auction,
                           "highest_bid": highest_bid,
                           "comments": comments, "watching": watching,
                           "comments_form": CommentsForm(new_comment)})

        new_comment.save(request.user, auction)
        return HttpResponseRedirect(reverse("auction", args=[auction.id]))

    if request.method == "POST" and "bid" in request.POST:
        b = float(request.POST["bid"])
        if b <= auction.price:
            return render(request, "auctions/auction.html",
                          {"auction": auction,
                           "highest_bid": highest_bid,
                           "comments": comments, "watching": watching,
                           "comments_form": CommentsForm()})

        bid = Bids(bid=b, auction=auction, user=request.user)
        bid.save()
        return HttpResponseRedirect(reverse("auction", args=[auction.id]))

    if request.method == "POST" and "add" in request.POST:
        user = User.objects.get(id=request.user.id)
        user.watchlist.add(auction)
        user.save()
        watching = True

    if request.method == "POST" and "rem" in request.POST:
        user = User.objects.get(id=request.user.id)
        user.watchlist.remove(auction)
        user.save()
        watching = False

    return render(request, "auctions/auction.html",
                  {"auction": auction,
                   "highest_bid": highest_bid,
                   "comments": comments, "watching": watching,
                   "comments_form": CommentsForm()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

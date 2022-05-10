from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListingForm, BidForm
from auctions.apps import AuctionsConfig
from django.contrib.auth.decorators import login_required
from .models import Category, Comment, Listing, User
wantedList = []

def index(request):
    data = set()
    for item in Category.objects.all():
        data.add(item.category)
    
    return render(request, "auctions/index.html", {
        "availableItem" : Listing.objects.filter(avai=True),
        "avaiCategory" : data
    })


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

@login_required(login_url='login')
def createListing(request):
    return render(request,"auctions/createListing.html",{
        "listingForm": CreateListingForm()
    })

@login_required(login_url='login')
def listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            url = form.cleaned_data["url"]
            bid = form.cleaned_data["bid"]
            category = form.cleaned_data["category"]
            user = request.user
            temp = Category.objects.create(category = category)
            temp.save()
            Listing.objects.create(user = user, item = title, description = description, 
            price = bid, url = url, category = temp, avai = True)
    

        return HttpResponseRedirect(reverse('index'))
        

    else:
        return render(request, "auctions/createListing.html")
        

def display(request,id):
    item = Listing.objects.get(id = id)
    bidForm = BidForm(request.POST)
    return render(request, "auctions/display.html",{
        "item" : item,
        "bidForm" : bidForm,
        "comments" : Comment.objects.filter(item=item)
    })

@login_required(login_url='login')
def watchlist(request):

    if request.method == "POST":
        id = request.POST["item"]
    
        item = Listing.objects.get(id = id)

        wantedList.append(item)
    
    
    return render(request, "auctions/watchlist.html", {
        "wantedItem" : wantedList
    })

@login_required(login_url='login')
def bid(request):
    bidForm = BidForm(request.POST)
    if request.method == "POST":
        id = request.POST["item"]
        bidValue = float(request.POST["bidValue"])
        
        item = Listing.objects.get(id = id)

        if bidValue > float(item.price):
            item.price = bidValue
            item.bidder = request.user
            item.save()
        else:
            return render(request, "auctions/display.html",{
                "item" : item,
                "bidForm" : bidForm,
                "message" : f"{item.winner} ,Your Bid was invalid",
                "winner" : False,
            })
            
        return render(request, "auctions/display.html",{
        "item" : item,
        "bidForm" : bidForm,
        "message" :  f"{item.winner} ,Your Bid was sucessfully submitted",
        "winner" : False,
    })



def close(request):

    if request.method == "POST":
            id = request.POST["item"]

            item = Listing.objects.get(id = id)

            if item.user == request.user:
                item.avai = False
                item.save()
                return render(request, "auctions/display.html",{
                    "item" : item,
                    "winner" : True,
            })
            else:
                return HttpResponse("you can't close this item")

def comment(request):
    if request.method == "POST":
        comment = (request.POST.get('content', False))
        itemid = int(request.POST.get('item', False))
        HttpResponse(itemid)
        print(itemid)
        print(comment)
        item = Listing.objects.get(pk = itemid)
        
        user = request.user
        

        Comment.objects.create(commenter=user, item = item, comment = comment)
        
        return render(request, "auctions/display.html",{
            "item" : item,
            "comments" : Comment.objects.filter(item=item),
        })


def sold(request):
    return render(request, "auctions/sold.html",{
            "soldItem" : Listing.objects.filter(avai= False)
        })

def category(request):
    category = request.POST["category"]

    temp_cate = Category.objects.get(category = category)
    return render(request, "auctions/category.html",{
        "itemList" : Listing.objects.filter(category = temp_cate)
    })
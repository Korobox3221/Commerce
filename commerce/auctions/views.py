from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Listings, Category, User, Bids, Watchlist, Comments
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def index(request):
    winner = Bids.objects.select_related('bider_Name').order_by('-bid')

    return render(request, "auctions/index.html", {"listings":Listings.objects.filter(isActive=True), 'winner':winner})

def create_listing(request):
    if request.method =="POST":
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        image = request.POST['image']
        owner = request.user
        category_obj, created = Category.objects.get_or_create(categoryName=category)
        listings = Listings(name = name, description = description, price = price, image = image, owner = owner, category = category_obj)
        listings.save()
        return HttpResponseRedirect(reverse("index"))


    return render(request, "auctions/create_listing.html")

@csrf_exempt
@login_required
def listing_page(request, title):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'watchlist':
            listing = get_object_or_404(Listings, name = title)
            user = request.user

            watch_item, created = Watchlist.objects.get_or_create(
                user=user,
                listing=listing,
                defaults={'added_at': timezone.now()})
            if not created:
                watch_item.delete()
            return HttpResponseRedirect(f'/watchlist/{user}')

        elif action == 'bid':
            bid = request.POST['bid']
            bider_Name = request.user
            listing_Name = Listings.objects.get(name = title)
            if listing_Name.highest_bid:
                if float(bid) <= listing_Name.highest_bid:
                    message = 'Invalid bid amount'
                    return HttpResponseRedirect(f'/error/{message}')
            else:
                if float(bid) < listing_Name.price:
                    message = 'Invalid bid amount'
                    return HttpResponseRedirect(f'/error/{message}')

            bids = Bids(bid = bid, listing_Name = listing_Name, bider_Name = bider_Name)
            listing_Name.highest_bid = bid
            listing_Name.save()
            bids.save()
        elif action == 'close_auction':
            listing = Listings.objects.get(name = title)
            listing.isActive = False
            listing.save()
        elif action == 'comment':
            comment = request.POST['comments']
            listing = Listings.objects.get(name = title)
            user = request.user
            com = Comments(lot = listing, commenter = user, comment = comment)
            com.save()
    if Listings.objects.filter(name = title).exists():
        listing = get_object_or_404(Listings, name=title)
        price = float(listing.price + 1)
        user = request.user
        is_in_watchlist = Watchlist.objects.filter(user=user, listing=listing).exists()
        highest_bid = Bids.objects.filter(listing_Name=listing).order_by('-bid').first()
        comment = Comments.objects.filter(lot = listing)
        count = comment.count()
        return render(request, 'auctions/listing_page.html',
                      {'title' : title,
                       "listing":listing,
                       'price': price,
                       'is_in_watchlist': is_in_watchlist,
                       'user': user,
                       'winner': highest_bid,
                       'comments': comment,
                       'count': count})
    else:
        message = 'No such listing'
        return HttpResponseRedirect(f'/error/{message}')



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


def error(request, message):
    return render(request, 'auctions/error.html', {
        'message': message
    })

def wishlist(request, username):
        user = get_object_or_404(User, username=username)
        watchlist_items = Watchlist.objects.filter(user=user).select_related('listing')
        return render(request, 'auctions/watchlist.html',{
            'watchlist': watchlist_items,
            'user': user
        })

def categories(request):
    return render (request, 'auctions/categories.html',  {"categories":Category.objects.all()})

def category(request, category):
    if Category.objects.filter(categoryName = category).exists():
        category_obj = get_object_or_404(Category, categoryName=category)
        category_items = Listings.objects.filter(category=category_obj, isActive=True)
        return render(request, 'auctions/category.html',{'category': category,
                                                         'listings':category_items})
    message = 'No such category'
    return HttpResponseRedirect(f'/error/{message}')


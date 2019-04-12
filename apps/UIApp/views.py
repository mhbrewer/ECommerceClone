##### E-Commerce Website Clone
##### Mason Brewer
##### March 16th, 2019

from django.shortcuts import render, redirect
from time import gmtime, strftime
import random, datetime, bcrypt
# from .models import User, Order
from django.contrib import messages
from apps.UIApp.models import User, Order
from apps.AdminApp.models import Category, Product


# GET: Loads the home page.
def homePage(request):
    if not request.session["loggedIn"]:
        return redirect("/login")
    else:
        context = {
            "user": User.objects.get(id = request.session["currentUserId"]),
            "allCats": Category.objects.all(),
        }
        return render(request, 'UIApp/home.html', context)
# GET: Loads Login/Reg Page page.
def loginPage(request):
    if request.session["loggedIn"]:
        return redirect("/")
    else:
        return render(request, 'UIApp/loginReg.html')
# POST: Processes a login request.
def loginProcess(request):
    if request.method == "GET":
        return redirect("/login")
    if request.method == "POST":
        errors = User.objects.loginValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/login")
        else:
            request.session['currentUserId'] = User.objects.get(email = request.POST['email']).id
            request.session["loggedIn"] = True
            return redirect("/")
# POST: Processes a registration request.
def regProcess(request):
    if request.method == "GET":
        return redirect("/login")
    if request.method == "POST":
        errors = User.objects.registerValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/login")
        else:
            newPassHash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            newUser = User.objects.create(firstName=request.POST["firstName"], lastName=request.POST["lastName"], 
                email=request.POST["email"], passHash = newPassHash.decode())
            request.session["currentUserId"] = newUser.id
            request.session["loggedIn"] = True
            return redirect("/")
# GET: Loads a category page.
def catPage(request, catId):
    if not request.session["loggedIn"]:
        return redirect("/login")
    else:
        thisCat = Category.objects.get(id = catId)
        context = {
            "catItems": Product.objects.filter(category = thisCat)
        }
        return render(request, 'UIApp/category.html', context)
# GET: Loads a specific item's page.
def itemPage(request, itemId):
    if not request.session["loggedIn"]:
        return redirect("/login")
    else:
        return render(request, 'UIApp/item.html')
# POST: Adds an item to the current order, or creates a new order.
def addToCart(request):
    pass
# GET: Loads the checkout/payment page.
def checkoutPage(request):
    if not request.session["loggedIn"]:
        return redirect("/login")
    else:
        return render(request, 'UIApp/checkout.html')
# POST: Processes the current order.
def checkoutProcess(request):
    pass
# POST: Logging a user out.
def logout(request):
    request.session["loggedIn"] = False
    return redirect("/login")
# POST: Just to make it easier to log in.
def mumsTheWord(request):
    if len(User.objects.filter(firstName = "mum").__dict__) == 0:
        pH = bcrypt.hashpw("Password1!".encode(), bcrypt.gensalt())
        newMum = User.objects.create(firstName="mum", lastName="isTheWord", email="secret@password.shh", 
            passHash=pH.decode())
        request.session["loggedIn"] = True
        request.session["currentUserId"] = newMum.id
        return redirect("/")
    else:
        mum = User.objects.get(firstName = "mum")
        request.session["loggedIn"] = True
        request.session["currentUserId"] = mum.id
        return redirect("/")


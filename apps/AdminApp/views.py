##### E-Commerce Website Clone
##### Mason Brewer
##### April 5th, 2019

from django.shortcuts import render, redirect
from time import gmtime, strftime
import random, datetime, bcrypt
from .models import *
from django.contrib import messages
from decimal import Decimal
from apps.UIApp.models import User, Order


# GET: Loads the login page for workers.
def loginPage(request):
    if request.session.get("adminLoggedIn"):
        return redirect("/admin/orders")
    else:
        return render(request, 'AdminApp/login.html')
# POST: Processes a login request.
def loginProcess(request):
    if request.method == "GET":
        return redirect("/login")
    if request.method == "POST":
        errors = Admin.objects.loginValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/admin/login")
        else:
            request.session['currentAdminId'] = Admin.objects.get(email = request.POST['email']).id
            request.session["adminLoggedIn"] = True
            return redirect("/admin/orders")
# POST: Processes a login with parameters, a special case use.
def paramLogin(request, pHash):
    pass
# GET: Loads list of orders.
def ordersPage(request):
    if not request.session["adminLoggedIn"]:
        return redirect("/admin/login")
    else:
        context = {
            "admin": Admin.objects.get(id = request.session["currentAdminId"]),
            "orders": Order.objects.all()
        }
        return render(request, 'AdminApp/orders.html', context)
# GET: Loads list of products.
def productsPage(request):
    if not request.session["adminLoggedIn"]:
        return redirect("/admin/login")
    else:
        context = {
            "admin": Admin.objects.get(id = request.session["currentAdminId"]),
            "products": Product.objects.all()
        }
        return render(request, 'AdminApp/products.html', context)
# POST: Deletes product.
def productDelete(request):
    pass
# GET: Loads a specific order.
def orderViewPage(request, orderID):
    pass
# POST: Changes the status of the order.
def changeStatus(request):
    pass
# GET: Loads the create page for a product.
def productNewPage(request):
    context = {
        "categories": Category.objects.all()
    }
    return render(request, 'AdminApp/newProduct.html', context)
# POST: Submits the new product.
def productNewProcess(request):
    if request.method == "GET":
        return redirect("/admin/product/new")
    if request.method == "POST":
        postCopy = request.POST.copy()
        if postCopy["price"]:
            postCopy["price"] = Decimal(postCopy["price"])
        errors = Product.objects.newValidator(postCopy)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect("/admin/product/new")
        else:
            if postCopy["category"]:
                catInput = Category.objects.get(id = postCopy["category"])
            Product.objects.create(name = postCopy["name"], description = postCopy["description"], 
                price = postCopy["price"], imageURL = postCopy["imageURL"], 
                category = catInput)
            return redirect("/admin/products")
# GET: Loads the edit page for a product.
def productEditPage(request):
    return render(request, 'AdminApp/editProduct.html')
# POST: Submits the edit of a product.
def productEditProcess(request):
    pass
# POST: Add a new Category.
def categoryNewProcess(request):
    if request.method == "GET":
        return redirect("/admin/product/new")
    if request.method == "POST":
        errors = Category.objects.newValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/admin/product/new")
        else:
            Category.objects.create(title = request.POST["title"])
            return redirect("/admin/product/new")
# GET: Shows all of the administrator accounts (subject to change).
def adminsPage(request):
    if not request.session["adminLoggedIn"]:
        return redirect("/admin/login")
    else:
        context = {
            "admin": Admin.objects.get(id = request.session["currentAdminId"]),
            "admins": Admin.objects.all()
        }
        return render(request, 'AdminApp/admins.html', context)
# GET: Loads admin add page.
def adminNewPage(request):
    return render(request,'AdminApp/newAdmin.html')
# POST: Submits the new admin.
def adminNewProcess(request):
    if request.method == "GET":
        return redirect("/admin/admin/new")
    if request.method == "POST":
        errors = Admin.objects.registerValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/admin/admin/new")
        else:
            newPassHash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            newAdmin = Admin.objects.create(accessLevel = int(request.POST["accessLevel"]), 
                firstName = request.POST["firstName"], lastName = request.POST["lastName"], 
                email = request.POST["email"], passHash = newPassHash.decode())
            request.session["currentAdminId"] = newAdmin.id
            request.session["adminLoggedIn"] = True
            return redirect("/admin/admins")
# POST: Logging an administrator out.
def logout(request):
    request.session["adminLoggedIn"] = False
    return redirect("/admin/login")
# POST: Creating the first admin.
def admumsTheWord(request):
    if len(Admin.objects.filter(firstName = "admum").__dict__) == 0:
        pH = bcrypt.hashpw("Password1!".encode(), bcrypt.gensalt())
        newAdmum = Admin.objects.create(accessLevel=3, firstName="admum", lastName="isTheWord", 
            email="secret@password.shh", passHash=pH.decode())
        request.session["adminLoggedIn"] = True
        request.session["currentAdminId"] = newAdmum.id
        print("MAKING ACCOUNT")
        return redirect("/admin/orders")
    else:
        print("ACCOUNT EXISTS")
        admum = Admin.objects.get(firstName = "admum")
        print(admum.email)
        request.session["adminLoggedIn"] = True
        request.session["currentAdminId"] = admum.id
        return redirect("/admin/orders")

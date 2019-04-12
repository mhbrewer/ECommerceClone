# E-Commerce Website Clone - Administrator App
# Mason Brewer
# March 13th, 2019

from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from decimal import Decimal

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Password verification helper functions.
def emailDoesExist(email):
    allAdmins = Admin.objects.all()
    if len(allAdmins) == 0:
        return False
    for user in allAdmins:
        if(email == user.email):
            return True
    return False
def hasNum(string):
    for i in range(0, len(string), 1):
        if string[i].isdigit():
            return True
    return False
def hasUpper(string):
    for i in range(0, len(string), 1):
        if string[i].isupper():
            return True
    return False
def hasLower(string):
    for i in range(0, len(string), 1):
        if string[i].islower():
            return True
    return False
def hasSpec(string):
    specs = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '?', '-', '_', '+', '=', '~']
    for i in range(0, len(string), 1):
        if string[i] in specs:
            return True
    return False
# For Logging in
def isPassCorrect(thisEmail, password):
    user = Admin.objects.get(email = thisEmail)
    return bcrypt.checkpw(password.encode(), user.passHash.encode())

# Admin Account Validators and Model
class AdminManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        if not postData.get('accessLevel', False):
            errors["accessLevel"] = "Please select an access level."
        else:
            if int(postData["accessLevel"]) > 3 or int(postData["accessLevel"]) < 1:
                errors["accessLevel"] = "Access Level must be between 1 and 3."
        if not postData["firstName"]:
            errors["firstName"] = "Please enter a first name."
        else:
            if len(postData["firstName"]) < 2:
                errors["firstName"] = "First name must be 2 or more characters."
        if not postData["lastName"]:
            errors["lastName"] = "Please enter a last name."
        else:
            if len(postData["lastName"]) < 2:
                errors["lastName"] = "Last name must be 2 or more characters."
        if not postData["email"]:
            errors["email"] = "Please enter an email."
        else:
            if not EMAIL_REGEX.match(postData["email"]):
                errors["email"] = "Invalid email address."
            if emailDoesExist(postData["email"]):
                errors["email"] = "That email is already associated with an account."
        if not postData["password"]:
            errors["password"] = "Please enter a password."
        else:
            if not hasNum(postData["password"]):
                errors["password"] = "Password must have a number."
            if not hasUpper(postData["password"]):
                errors["password"] = "Password must have an upper-case letter."
            if not hasLower(postData["password"]):
                errors["password"] = "Password must have a lower-case letter."
            if not hasSpec(postData["password"]):
                errors["password"] = "Password must have a special character."
        if(not postData["passwordRepeat"]):
            errors["passwordRepeat"] = "Please repeat your password."
        else:
            if postData["password"] != postData["passwordRepeat"]:
                errors["passwordRepeat"] = "Passwords no not match."
        return errors
    def loginValidator(self, postData):
        errors = {}
        if not postData["email"]:
            errors["email"] = "Please enter your email."
        else:
            if not emailDoesExist(postData["email"]):
                errors["email"] = "Email does not exist."
        if not postData["password"]:
            errors["password"] = "Please enter your password."
        else:
            if emailDoesExist(postData["email"]) and not isPassCorrect(postData["email"], postData["password"]):
                errors["password"] = "Invalid password."
        return errors
class Admin(models.Model):
    accessLevel = models.IntegerField()
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    email = models.CharField(max_length = 255)
    passHash = models.CharField(max_length = 255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = AdminManager()


# Product Validators and Model
class ProductManager(models.Manager):
    def newValidator(self, postData):
        errors = {}
        if not postData["name"]:
            errors["name"] = "Please enter a name for the item."
        else:
            if len(postData["name"]) < 2:
                errors["name"] = "Item name must be 2 or more characters."
        if not postData["description"]:
            errors["description"] = "Please enter a description for the item."
        else:
            if len(postData["description"]) < 2:
                errors["description"] = "Description must be 2 or more characters."
        if not postData["price"]:
            errors["price"] = "Please enter a price for the item."
        else:
            # Price entry must be converted to a float or decimal before input.
            if postData["price"] <= 0:
                errors["price"] = "Item price must be positive."
        return errors
class Product(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    imageURL = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("Category", related_name="category", on_delete=models.PROTECT)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = ProductManager()


# Catagory (for products) Validators and Model
class CategoryManager(models.Manager):
    def newValidator(self, postData):
        errors = {}
        if not postData["title"]:
            errors["title"] = "Must enter in a category name."
        else:
            if len(postData["title"]) < 2:
                errors["title"] = "Title must be 2 or more characters."
        return errors
class Category(models.Model):
    title = models.CharField(max_length = 50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = CategoryManager()

# E-Commerce Website Clone - User Interface App
# Mason Brewer
# March 13th, 2019

from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Password verification helper functions.
def emailDoesExist(email):
    allUsers = User.objects.all()
    if len(allUsers) == 0:
        return False
    for user in allUsers:
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
    user = User.objects.get(email = thisEmail)
    return bcrypt.checkpw(password.encode(), user.passHash.encode())

# User Validators and Model
class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        if not postData["firstName"]:
            errors["firstName"] = "Please enter a first name."
        else:
            if(len(postData["firstName"]) < 2):
                errors["firstName"] = "First name must be 2 or more characters."
        if not postData["lastName"]:
            errors["lastName"] = "Please enter a last name."
        else:
            if(len(postData["lastName"]) < 2):
                errors["lastName"] = "Last name must be 2 or more characters."
        if not postData['email']:
            errors['email'] = "Please enter an email address."
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
        if not postData["passwordRepeat"]:
            errors["passwordRepeat"] = "Please re-enter your password."
        else:
            if postData["password"] != postData["passwordRepeat"]:
                errors["passwordRepeat"] = "Passwords no not match."
        return errors
    def loginValidator(self, postData):
        errors = {}
        if not postData["email"]:
            errors["loginEmail"] = "Please enter an email."
        else:
            if not emailDoesExist(postData["email"]):
                errors["loginEmail"] = "Email does not exist."
        if not postData["password"]:
            errors["loginPassword"] = "Please enter a password."
        else:
            if emailDoesExist(postData["email"]) and not isPassCorrect(postData["email"], postData["password"]):
                errors["loginPassword"] = "Invalid password."
        return errors
class User(models.Model):
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    email = models.CharField(max_length = 255)
    passHash = models.CharField(max_length = 255)
    cart = models.ManyToManyField("AdminApp.Product", related_name="carter")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager()


# Order Validators and Model
class OrderManager(models.Manager):
    def newValidator(self, postData):
        # Not neccessary at the moment.
        errors = {}
        return errors
class Order(models.Model):
    orderer = models.ForeignKey("User", related_name="orderer", on_delete=models.PROTECT)
    billingAdd = models.CharField(max_length = 255)
    shippingAdd = models.CharField(max_length = 255)
    status = models.CharField(max_length = 50)
    dateSubmitted = models.DateTimeField()
    products = models.ManyToManyField("AdminApp.Product", related_name="products")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = OrderManager()

from django.db import models
from datetime import date, datetime
# validation and authintication file which had made by Ali
from .ValidAuth import *
"""
sigeUP:::

firstName_signUp
lastName_signUp
email_signUp
password_signUp
confirmPassword_signUp
_________________________
Login::::
email_login
password_login

"""
# This is the Vaildation


class UsersManager(models.Manager):
    def basic_validator(self, postData):  # for testing
        errors = {}
        # vaildation for SignUp
        # first name characters only and more at least 2 characters
        if not isItValidName(str(postData["firstName_signUp"])):
            errors["firstName_signUp"] = "Please Enter Your Real First Name"
        # last name characters only and more at least 2 characters
        if not isItValidName(str(postData["lastName_signUp"])):
            errors["lastName_signUp"] = "Please Enter Your Real Last Name"
        # is the Email in Email fromat ?
        if not isItValidEmail(str(postData["email_signUp"])):
            errors["email_signUp"] = "Please Enter Valid Email"
        # check the Email not exisit in DB
        if len(Users.objects.filter(email=str(postData["email_signUp"]).lower())) > 0:
            errors["email_signUp"] = "This Email Already Reigistered || Email already in DB"
        # password must be VERY STRONG
        # length minimum 8 characters at least one digit, lowerrcase, uppercase, and special
        if not isVeryStrongPassword(str(postData["password_signUp"])):
            errors["password_signUp"] = "Password Must be : length minimum 8 characters. at least one digit, lowerrcase, uppercase, and special"

        # check the password is same for confirmation
        if str(postData["password_signUp"]) != str(postData["confirmPassword_signUp"]):
            errors["confirmPassword_signUp"] = "Password is not same"

        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255, null=True)
    password = models.TextField()
    is_admin = models.BooleanField(default=False)
    # for Vaildation part
    objects = UsersManager()


class Reports(models.Model):
    verbose_msg = models.TextField()
    md5 = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=255)
    sha256 = models.CharField(max_length=256)
    scan_date = models.DateTimeField()
    permalink = models.TextField()
    positives = models.IntegerField()
    total = models.IntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Scan(models.Model):
    name = models.CharField(max_length=50)
    detected = models.BooleanField()
    version = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    update = models.IntegerField()
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)

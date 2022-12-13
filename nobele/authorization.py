from . import models,additional

from django.core.mail import send_mail
from django.conf import settings
import random


def check_existence(email : str) -> bool:
    try:
        models.Account.objects.get(email=email)
        return True
    except:
        return False

def register_account(*args, **kwargs):

    email = kwargs.pop('email')
    password = kwargs.pop('password')
    name = kwargs.pop('name')
    surname = kwargs.pop('surname')
    password = additional.hash_password(password)

    models.Account.objects.create(password=password,email=email,name=name,surname=surname)

def login_into_account(email : str , password : str):
    try:
        account = models.Account.objects.get(email = email)
    except:
        return False

    password = additional.hash_password(password)
    if account.password == password:
        return True
    else:
        return False

def save_session(email : str , ip : str):
    account = models.Account.objects.get(email=email)
    models.Session.objects.create(account=account,ip=ip)

def quit_session(email : str , ip : str):
    account = models.Account.objects.get(email=email)
    models.Session.objects.get(account=account,ip=ip).delete()

def check_session(ip : str):
    try:
        session = models.Session.objects.get(ip=ip)
        return (session , True)
    except:
        return (None, False)

def get_token(email : str):
    try:
        token = pull_token(email)
    except:
        token = random.randrange(100,999)
        models.VerificationToken.objects.create(email=email,token=token)
    return token

def check_token(email : str , token : str):

    db_token = pull_token(email)
    if db_token == int(token):
        return True
    return False

def verify_account(email : str):
    account = models.Account.objects.get(email=email)
    account.verified = True
    account.save()
    models.VerificationToken.objects.get(email=email).delete()

def pull_token(email : str):
    account = models.VerificationToken.objects.get(email=email)
    return account.token

def email_send(email : str , title : str , description : str):
    send_mail(title,description,settings.EMAIL_HOST_USER,[email])

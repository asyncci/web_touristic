from . import models
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import datetime

def rand_sender(name,email,ip):
    if register(name,email,ip):
        veriftokens = models.VerifToken.objects
        try:
            token = veriftokens.get(email=email).token
        except ObjectDoesNotExist:
            token = random.randrange(100,999)
            veriftokens.create(email=email,token=token)

        send_mail('Around the World','Verification token is: '+ str(token),settings.EMAIL_HOST_USER,[email])
        return (False,True)
    
    return (True,False)

def register(name,email,ip):
    try:
        account = models.Account.objects.get(email=email)        
    except ObjectDoesNotExist:
        account = models.Account.objects.create(ip=ip,name=name,email=email)

    return account.verified == False        

def check_token(token,email):
    veriftoken = models.VerifToken.objects.get(email=email)
    if int(token) == veriftoken.token:
        veriftoken.delete()
        veriftoken.save()
        account = models.Account.objects.get(email=email)
        account.verified = True
        account.verif_date = datetime.date.today()
        account.save()
        return True
    return False

def reset_verif(account: models.Account):
    account.verif_date = None
    account.verified = False
    account.save()

def check_verification(ip):
    account = models.Account.objects.get(ip=ip)
    days = (datetime.date.today() - account.verif_date).days
    if days >= 30:
        reset_verif(account)
        return False
    return True

def test(ip):
    # account = models.Account.objects.get(ip=ip)
    # print(ip)
    # reset_verif(account)
    # print(datetime.date.today())
    # print((datetime.date(2022,12,5) - datetime.date(2022,11,5)).days)
    pass
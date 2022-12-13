from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import generic
from django import views
from . import forms, authorization,models
from django.views.decorators import csrf
from ipware import get_client_ip
from django.http import HttpResponse, HttpRequest
# Create your views here.

def main_page(request):
    (ip,_) = get_client_ip(request)

    (session, authorized) = authorization.check_session(ip)

    verified = None

    if not session == None:
        verified = session.account.verified
        
    countries = models.Country.objects.all()

    context = {
        'countries':countries,
        'verified': verified, 
        'authorized':authorized
        }

    return render(request,'nobele/main.html',context)

def login_page(request):
    success = True
    if request.method == "POST":
        form = forms.LoginAccountForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            (ip,_) = get_client_ip(request)

            if authorization.login_into_account(email,password):
                authorization.save_session(email,ip)
                return redirect(reverse('nobele:main'))
            else:
                success = False
    form = forms.LoginAccountForm()

    return render(request,'nobele/login_page.html',{'form':form, 'success':success})

@csrf.csrf_protect
def logout_from_account(request):
    email = request.POST.get('email')
    (ip,_) = get_client_ip(request)

    authorization.quit_session(email,ip)
    return redirect(reverse('nobele:login'))

@csrf.csrf_protect
def register_page(request):
    form = forms.RegisterAccountForm()
    verif = False
    if request.method == "POST":
        form = forms.RegisterAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            repeat_email = form.cleaned_data['repeat_email']
            
            if not authorization.check_existence(email):
                password = form.cleaned_data['password']
                repeat_password = form.cleaned_data['repeat_password']
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                
                if email == repeat_email :
                    if password == repeat_password:
                        token = authorization.get_token(email)
                        (ip,_) = get_client_ip(request)
                        authorization.register_account(email=email,password=password,name=name,surname=surname)
                        authorization.email_send(title="Around the World verification",description="Your token: "+str(token),email=email)
                        verif = True
                    else:
                        return render(request,'nobele/register_page.html',{'form':form,'verif':verif,'comment':'password is not same'})
                else:
                    return render(request,'nobele/register_page.html',{'form':form,'verif':verif,'comment':'email is not same'})
            else:
                return render(request,'nobele/register_page.html',{'form':form,'verif':verif,'comment':'account exists'})
    return render(request,'nobele/register_page.html',{'form':form, 'verif':verif ,'comment':''})


@csrf.csrf_protect
def verify(request):
    if request.method == "POST":    
        email = request.POST.get('email')
        token = request.POST.get('token')
        if authorization.check_token(email,token):
            authorization.verify_account(email)
        else:
            return HttpResponse("Not correct token")

    # return render(request,'nobele/verif_page.html',{'form':form,'url':'nobele:verify','email':email})    
    return redirect(reverse('nobele:main'))

@csrf.csrf_protect
def verificate_manually(request):
    return render(request,'nobele/verif_page.html')

def user_page(request):
    (ip,_) = get_client_ip(request)
    session = models.Session.objects.get(ip=ip)
    
    context = {
        'user':session.account,
        'comments':[]
    }

    return render(request,'nobele/user_page.html',context)


class CountryView(generic.DetailView):
    queryset = models.Country.objects.all()
    template_name = "nobele/touring/country_specific.html"
    session = False

    def setup(self, request, *args, **kwargs):
        (ip,_) = get_client_ip(request)
        self.session = authorization.check_session(ip)
        return super().setup(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        context['cities'] = models.City.objects.filter(country = obj)
        context['authorized'] = self.session[1]
        context['account'] = self.session[0] 
        print(obj.pk)
        context['comments'] = models.Comment.objects.filter(country=obj)
        context['comment_form'] = forms.CommentForm()   
        return context
    
class CityView(generic.DetailView):
    queryset = models.City.objects.all()
    template_name = 'nobele/touring/city_specific.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        context['hotels'] = models.Hotel.objects.filter(city=obj)
        context['rate_form'] = forms.RateForm()
        return context
    
    
@csrf.csrf_protect
def rate_hotel(request,pk):
    if request.method == "POST":
        (ip,_) = get_client_ip(request)
        (session,is_valid) = authorization.check_session(ip)
        if not session.account.verified :
            return redirect(reverse('nobele:verificate'))
        if is_valid:
            form = forms.RateForm(request.POST)
            if form.is_valid():
                hotel = models.Hotel.objects.get(pk=pk)
                try:
                    hotel_rate = models.HotelRating.objects.get(hotel=hotel)
                except:
                    hotel_rate = models.HotelRating.objects.create(hotel=hotel,key=pk)

                hotel_rate.count += 1
                hotel_rate.summary += form.cleaned_data['rate']
                hotel_rate.save()

                hotel.stars = hotel_rate.summary / hotel_rate.count
                hotel.save()
        
        return redirect(request.META['HTTP_REFERER'])

def new_comment(request,pk):
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            (ip,_) = get_client_ip(request)
            (session,is_valid) = authorization.check_session(ip)
            if not session.account.verified :
                return redirect(reverse('nobele:verificate'))
            if is_valid:
                account = session.account
                text = form.cleaned_data['comment']
                country = models.Country.objects.get(pk=pk)
                models.Comment.objects.create(author=account,text=text,country=country)
            else:
                return redirect(reverse('nobele:login'))

    return redirect(reverse('nobele:country',args=[pk]))
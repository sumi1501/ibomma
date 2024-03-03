from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name='home.html'

class Tamil(TemplateView):
    template_name='Tamil.html'

class Hindi(TemplateView):
    template_name='Hindi.html'

class Enter_Page(TemplateView):
    template_name='Enter_Page.html'

class About(TemplateView):
    template_name='About.html'
    
class Bug(TemplateView):
    template_name='Bug.html'


def registration(request):
    umf=UserMF()
    pmf=ProfileMF()
    d={'umf':umf,'pmf':pmf}
    if request.method=='POST' and request.FILES:
        umfd=UserMF(request.POST)
        pmfd=ProfileMF(request.POST,request.FILES)
        if umfd.is_valid() and pmfd.is_valid():
            Nud=umfd.save(commit=False)
            submittedpw=umfd.cleaned_data['password']
            Nud.set_password(submittedpw)
            Nud.save()

            Npd=pmfd.save(commit=False)
            Npd.username=Nud
            Npd.save()

            return HttpResponse('Data Submitted')
    return render(request,'registration.html',d)



def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('Home'))
            else:
                return HttpResponse('Not active User')
    return render(request,'Login.html')

@login_required
def Change_pas(request):
    if request.method=='POST':
        pw=request.POST['password']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return render(request,'Enter_Page.html')
    return render(request,'Change_pas.html')


def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.POST['username']
        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Modify The password successfully')
        else:
            return HttpResponse('Username is not validate')
    return render(request,'reset_password.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))
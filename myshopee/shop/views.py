from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.shortcuts import render,redirect
from .models import Category,Product
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
def index(request):
    return render(request,'index.html')
def categories(request):
    item=Category.objects.all()
    return render(request,'categories.html',{'item':item})


def products(request,i):
    c=Category.objects.get(id=i)
    p=Product.objects.filter(p_category=c)
    return render(request,'products.html',{'c':c,'p':p})


def product_details(request,i):
    product=Product.objects.get(id=i)
    return render(request,'product_details.html',{'product':product})

def register(request):
    if (request.method == "POST"):  # after submission
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']
        if(cp==p):
            user = User.objects.create_user(username=u, password=p, first_name=fn, last_name=ln, email=e)
            user.save()
            return redirect('shop:index')
    return render(request, 'register.html')

def user_login(request):
    u = request.POST.get('u')
    p = request.POST.get('p')
    user = authenticate(username=u,password=p)
    if user:
        login(request,user)
        return redirect('shop:index')
    else:
        messages.error(request,'invalid credentials')

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:user_login')
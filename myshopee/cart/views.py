from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Payment,Order_table
import razorpay
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
# Create your views here.
@login_required
def addtocart(request,i):

    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.p_stock>0):
            cart.quantity +=1
            cart.save()
            p.p_stock -=1
            p.save()
    except:
        if(p.p_stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.p_stock +=1
            p.save()
    return redirect('cart:cart_view')

@login_required
def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price
    return render(request,'cart.html',{'cart':cart,'total':total})


def cart_decrement(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity -= 1
            cart.save()
            p.p_stock+=1
            p.save()
        else:
            cart.delete()
            p.p_stock+=1
            p.save()

    except:
        pass
    return redirect('cart:cart_view')


def remove(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.p_stock+=cart.quantity
        p.save()
    except:
        pass
    return redirect('cart:cart_view')


def continuee(request):
    return redirect('cart:cart_view')

def placeorder(request):
    if(request.method=="POST"):
        d = request.POST.get("d")
        b = request.POST.get("b")
        p = request.POST.get("p")
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)
        total=int(total*100)
        #create Razorpay client using our Api Credentials
        client=razorpay.Client(auth=('rzp_test_RmKKPLzJtt3vJW','YyiM8ViopIsXKP7rpWLs0YLO'))

        #Create Order
        response_payment=client.order.create(dict(amount=total,currency="INR"))
        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=="created":
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o = Order_table.objects.create(user=u,product=i.product,address=d,phone=p,pin=p,no_of_items=i.quantity,order_id=order_id,)
                o.save()
        response_payment['name']=u.username
        return render(request, 'placeorde.html',{'payment':response_payment})

    return render(request,'payment.html')


@csrf_exempt
def payment_done(request,u):
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request,user)

    if(request.method=="POST"):
        response = request.POST
        param_dict = {
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_4DuEprsTI3hLDn','vD0pR11FtGaldbHotwEakO44'))
        try:
            status = client.utility.verify_payment_signature(param_dict)

            ord = Payment.objects.get(order_id = response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id']
            ord.paid = True
            ord.save()

            u = User.objects.get(username=u)
            c = Cart.objects.filter(user=u)
            o = Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="paid"
                i.save()
            c.delete()
            return render(request, 'payment_done.html',{'status':True})
        except:
            return render(request, 'payment_done.html',{'status':False})
    return render(request,'payment_done.html')


@login_required
def your_orders(request):
    user=request.user
    orders = Order_table.objects.filter(payment_status="paid",user=user)
    return render(request,'your_orders.html',{'orders':orders,'user':user.username})

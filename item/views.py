from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem, OrderInfo
import json
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm

UserModel = get_user_model()

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = set([prod.category for prod in products])
    allprods = {}
    for cats in categories:
        prods = []
        for prod in products:
            if prod.category == cats:
                prods.append(prod)
        allprods[cats] = prods
                
    return render(request, 'home.html', {'products':allprods})

def updatecart(request):
    data = json.loads(request.body)
    action = data.get('action')
    product = data.get('product')
    print(product)
    print(action)
    item = Product.objects.get(pk=product)
    order, created = Order.objects.get_or_create(receiver=request.user, ordered = False)
    print(f'order {order}')
    if order.items.filter(item__title=item.title).exists():
        orderitem = OrderItem.objects.filter(item=item).first()
        print(f'orderitem {orderitem}')
        print("inside first if")
        if action == 'add':
            orderitem.quantity += 1
            orderitem.save()                    
            order.items.add(orderitem)
        if action == 'decrease':
            orderitem.quantity -= 1
            orderitem.save()                    
            order.items.add(orderitem)
        if action =='remove' or orderitem.quantity == 0:
            orderitem.delete()
    else:
        orderitem = OrderItem.objects.create(customer=request.user, quantity=1, item=item)
        order.items.add(orderitem)

    data = {
        "cart_size":order.get_cart_size,
        "quantity":orderitem.quantity,
        "productid":item.slug,
        "grandtotal":order.get_grand_order_total()

    }    

    return JsonResponse(data)


@login_required
def cartsummaryview(request):
    oder = Order.objects.filter(receiver=request.user, ordered=False)
    if oder.exists():
        order = oder[0]
        orderitems = order.items.all()
        return render(request, 'ordersummary.html', {'order':orderitems,'Order':order})

    else:
        messages.warning(request, 'You have no items in your cart yet')
        return redirect('/') 


@login_required
def checkoutview(request):
    order = Order.objects.filter(receiver=request.user, ordered=False)
#   HANDLING POST REQUEST OF CHECKOUT VIEW

    if request.method =='POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = order[0]
            order.ordered = True
            order.save()

            # test
            instance = form.save(commit=False)
            instance.orderlist = order
            instance.user = request.user
            instance.save()
            messages.success(request, f"Your order has been sucessfully placed.You can track order using id {instance.orderid}")
            return redirect('/')

        else:
            messages.warning(request, "You have some error in submitting form")
            return render(request, 'checkout.html', {'form':form})           
    


#  HANDLING GET REQUEST OF CHECKOUT VIEW
    if order.exists():
        form = CheckoutForm(initial={'Email':request.user.email})
        order = order[0]
        return render(request, 'checkout.html', {'form':form})           

    else:
        messages.warning(request, "You have not placed any order yet")
        return redirect('/')


# Order Tracker view
def trackorderview(request):
    if request.method == 'POST':
        orderid = request.POST.get('orderid')
        orderinfo = OrderInfo.objects.filter(orderid=orderid)
        if orderinfo.exists():
            message = orderinfo.messages
            return render(request, 'tracker.html', {'messages':messages})
        else:
            messages.warning(request, "No order matched with your provided orderid . Please type correct order id")
            return redirect('/tracker/')


    return render(request, 'tracker.html')







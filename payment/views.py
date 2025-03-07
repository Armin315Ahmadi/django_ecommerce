from django.shortcuts import render, redirect


from cart.cart import Cart
from .forms import ShippingForm , ShippingAddress ,PaymentForm
from .models import  ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product ,Profile
import datetime
# Create your views here.



def orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get the order items
        items = OrderItem.objects.filter(id=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # check if true or false
            if status =="true":
                # get the order
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(shipped=True , date_shipped=now)
            else:
                # get the order
                order = Order.objects.filter(id=pk)
                # update the status
                order.update(shipped=False)
            messages.success(request,"shipping status updated.")
            return redirect('home')



        return render(request, "orders.html", {"orders":order , "item":items})



    else:
        messages.success(request, "Access Denied.")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            # grab order
            order = Order.objects.filter(id=num)

            order = Order.objects.filter(id=num)

            # grab date and time
            now = datetime.datetime.now()
            # update order
            orders.update(shipped=True, date_shipped=now)

            messages.success(request, "shipping status updated.")
            return redirect('home')

        return render(request, "not_shipped_dash.html", {"orders":orders})

    else:
        messages.success(request, "Access Denied.")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            # grab date and time
            now = datetime.datetime.now()
            # update order
            orders.update(shipped=False)

            messages.success(request, "shipping status updated.")
            return redirect('home')

        return render(request, "shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied.")
        return redirect('home')


def process_order(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get('my_shipping')


        # gather order info
        full_name = my_shipping['shpping_full_name']
        email = my_shipping['shipping_email.']
        # create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals

        # create an order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # create order
            create_order = Order(user=user , full_name=full_name , email=email, shipping_address=shipping_address , amount_paid=amount_paid)
            create_order.save()
            # add order items
            # get the order id
            order_id = create_order.pk
            # get product info
            for product in cart_products():
                # get product id
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                    # get quantity
                for key , value in quantities().items():
                    if int(key) == product.id:
                        #value
                        create_order_item = OrderItem(order_id=order_id  ,product_id=product_id , user=user,quantity=value,price=price)
                        create_order_item.save()

            # delete the cart
            for key in list(request.session.key()):
                if key == "session_key":
                    # delete the key
                    del request.session[key]

            # delete cart from database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # delete shopping cart in database( old_cart field)
            current_user.update(old_cart="")








            messages.success(request, "order placed!.")
            return redirect('home')

        else:
            # not logged in
            # create order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()

            # get the order id
            order_id = create_order.pk
            # get product info
            for product in cart_products():
                # get product id
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                    # get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # value
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id,
                                                      quantity=value, price=price)
                        create_order_item.save()

            # delete the cart
            for key in list(request.session.key()):
                if key == "session_key":
                    # delete the key
                    del request.session[key]




        messages.success(request , "order placed!.")
        return redirect('home')







    else:
        messages.success(request , "Access denied")
        return redirect('home')

def billing_info(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if the user is login
        if request.user.is_authenticated:
            # get the billing
            billing_form = PaymentForm()
            return render(request, "billing_info.html",
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST , "billing_form":billing_form})
        else:
            #not log in
            return render(request, "billing_info.html",
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                           "shipping_info": request.POST , "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "billing_info.html",
                      {"cart_products": cart_products, "quantities": quantities, "totals": totals,
                       "shipping_form": shipping_form})
    else:
        messages.success(request , "Access denied")
        return redirect('home')


def checkout(request):
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        if request.user.is_authenticated:
            # check out as login user
            #shipping form
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            #shipping user
            shipping_form = ShippingForm(request.POST or None ,instance=shipping_user)
            return render(request, 'checkout.html',
                   {"cart_products": cart_products, "quantities": quantities, "totals": totals , "shipping_form":shipping_form})
        else:
            #checkout as guest
            shipping_form = ShippingForm(request.POST or None)
            return render(request, 'checkout.html',
                          {"cart_products": cart_products, "quantities": quantities, "totals": totals , "shipping_form":shipping_form})


def payment_success(request):
    return render(request, 'payment_success.html', {})

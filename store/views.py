from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from .utils import cookieCart, cartData, guestOrder

def homepage(request):
    return render (request = request, template_name='store/home.html')
def register_request(request):
			if request.method == "POST":
				form = NewUserForm(request.POST)
				if form.is_valid():
					user = form.save()
					login(request, user)
					messages.success(request, "Registration successful." )
					return redirect('/login')
				messages.error(request, "Unsuccessful registration. Invalid information.")
			form = NewUserForm()
			return render (request=request, template_name="store/register.html", context={"register_form":form})
def login_request(request):
			if request.method == "POST":
				form = AuthenticationForm(request, data=request.POST)
				if form.is_valid():
					username = form.cleaned_data.get('username')
					password = form.cleaned_data.get('password')
					user = authenticate(username=username, password=password)
					if user is not None:
						login(request, user)
						messages.info(request, f"You are now logged in as {username}.")
						return redirect('store')
					else:
						messages.error(request,"Invalid username or password.")
				else:
					messages.error(request,"Invalid username or password.")
			form = AuthenticationForm()
			return render(request=request, template_name="store/login.html", context={"login_form":form})
def logout_request(request):
		logout(request)
		messages.info(request, "You have successfully logged out.")
		return redirect("store:store")

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order  = data['order']
	items = data['items']
	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order  = data['order']
	items = data['items']
	context = {'items': items, 'order':order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order  = data['order']
	items = data['items']
	context = {'items': items, 'order':order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)
def woman(request):
    return render(request, 'store/images.html')

def man(request):
    return render(request, 'store/man.html')
def shoes(request):
    return render(request, 'store/shoes.html')

def view(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/view.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

#@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
from django.urls import path

from . import views
urlpatterns = [
    path("", views.homepage, name="homepage"),

    path("login/", views.login_request, name="login"),
    path("logout/", views.login_request, name="logout"),

    path("register/", views.register_request, name="register"),
	path('store/', views.store, name="store"),
 	path('woman/', views.woman ,name='woman'),
   	path('man/', views.man ,name='man'),
    path('shoes/', views.shoes ,name='shoes'),


	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('view/', views.view, name="view"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]
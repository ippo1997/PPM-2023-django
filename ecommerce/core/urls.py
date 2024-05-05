from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm
from .views import fantamatrimonio_page

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order-summary/', views.order_summary, name='order_summary'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),
    path('place-order/', views.place_order, name='place_order'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:index'), name='logout'),
    path('update-shipping-status/<int:pk>/', views.update_shipping_status, name='update_shipping_status'),
    path('fantamatrimonio/', views.fantamatrimonio_page, name='fantamatrimonio'),
]

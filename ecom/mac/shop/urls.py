from django.contrib import admin
from django.urls import path,include
from shop import views


urlpatterns = [
    path('', views.shop,name='shop'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('tracker/', views.tracker,name='tracker'),
    path('orderTracker/', views.orderTracker,name='orderTracker'),
    path('search/', views.search,name='search'),
    path('myorders/', views.myorders,name='myorders'),
    path('products/<int:id>', views.productview,name='productview'),
    path('checkout/', views.checkout,name='checkout'),
    path('wishlist/', views.wishlist,name='wishlist'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logouts/', views.logouts, name='logouts'),
    #path('handlerequest/', views.handlerequest,name='handlerequest'),
    
]
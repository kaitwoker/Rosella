from django.urls import path, include
from .views import bouquet_constructor, index, product_list, product_detail, about, search_products, contact

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('shop/', product_list, name='product_list'),
    path('shop/<slug:slug>/', product_detail, name='product_detail'),
    path('about/', about, name='about'),
    path('search/', search_products, name='search_products'),
    path('contact/', contact, name='contact'),
    path('user/', include('users.urls', namespace='users')),

    # ✅ Явно указываем маршрут для корзины, чтобы он не интерпретировался как категория
    path('cart/', include('cart.urls')),
    path('constructor/', bouquet_constructor, name='bouquet_constructor'),

    # ❗ Должно стоять в конце, чтобы не перехватывать cart/
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls')),  # Маршруты приложения пользователей
    path('accounts/', include('django.contrib.auth.urls')),
    path('favorites/', include('favorites.urls')),  # Маршруты избранного
    path('constructor/', include('constructor.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('main.urls')),  # Подключаем маршруты из приложения main (catch-all)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

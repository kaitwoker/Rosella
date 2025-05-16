from cart.models import CartItem
from django.conf import settings  # Добавляем импорт settings

def cart_context(request):
    cart_items = CartItem.objects.none()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return {
        'cart_items': cart_items,
        'cart_item_count': total_quantity,
        'cart_total_price': total_price,
    }

def favorites_context(request):
    favorite_count = 0
    # Проверяем установлено ли приложение favorites
    if 'favorites' in settings.INSTALLED_APPS and request.user.is_authenticated:
        from favorites.models import Favorite
        favorite_count = Favorite.objects.filter(user=request.user).count()
    
    return {
        'favorite_item_count': favorite_count,
    }
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from decimal import Decimal
from .models import Product, Category, Flower
from django.db.models import Q
from reviews.models import Review


def index(request):
    products_day = Product.objects.filter(is_deal=True)[:12]
    for product in products_day:
        product.old_price = product.price
        product.new_price = product.sell_price()
        product.profit = (product.old_price - product.new_price).quantize(Decimal("0.01"))
        
    discounted_products = Product.objects.filter(discount__gt=0)
    reviews = Review.objects.filter(approved=True).order_by('-created')[:4]

    return render(request, 'main/index/index.html', {
        'products_day': products_day,
        'discounted_products': discounted_products,
        'reviews': reviews,
    })


def about(request):
    return render(request, 'main/about/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def cart_detail(request):
    return render(request, 'main/cart/cart.html') 


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    images = product.images.all()

    # Добавляем отзывы
    approved_reviews = product.reviews.filter(approved=True)
    reviews_count = approved_reviews.count()

    return render(request, 'main/shop/detail.html', {
        'product': product,
        'images': images,
        'approved_reviews': approved_reviews,
        'reviews_count': reviews_count,
    })


def search_products(request):
    return HttpResponse("Поиск товаров")


def bouquet_constructor(request):
    return render(request, 'main/constructor.html')


def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    sort_option = request.GET.get('sort', 'default')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    query = request.GET.get('query', '')
    flower_filter = request.GET.getlist('flowers')
    selected_flower_ids = [int(flower_id) for flower_id in flower_filter if flower_id] if flower_filter else []

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if price_min and price_max:
        try:
            price_min = Decimal(price_min)
            price_max = Decimal(price_max)
            products = products.filter(price__gte=price_min, price__lte=price_max)
        except:
            pass

    if selected_flower_ids:
        products = products.filter(flowers__id__in=selected_flower_ids).distinct()

    sorting_options = {
        "price_desc": "-price",
        "price_asc": "price",
        "newest": "-created",
        "oldest": "created",
        "name_asc": "name",
        "name_desc": "-name",
    }
    if sort_option in sorting_options:
        products = products.order_by(sorting_options[sort_option])

    paginator = Paginator(products, 16)
    try:
        current_page = paginator.page(int(page))
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    flowers = Flower.objects.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'main/shop/product_list_ajax.html', {
            'category': category,
            'categories': categories,
            'products': current_page,
            'slug_url': category_slug,
            'current_sort': sort_option,
            'price_min': price_min,
            'price_max': price_max,
            'query': query,
            'flower_filter': flower_filter,
            'selected_flower_ids': selected_flower_ids,
            'flowers': flowers,
            'paginator': paginator,
        })

    return render(request, 'main/shop/shop.html', {
        'category': category,
        'categories': categories,
        'products': current_page,
        'slug_url': category_slug,
        'current_sort': sort_option,
        'price_min': price_min,
        'price_max': price_max,
        'query': query,
        'flower_filter': flower_filter,
        'selected_flower_ids': selected_flower_ids,
        'flowers': flowers,
        'paginator': paginator,
    })

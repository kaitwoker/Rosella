from django.contrib import admin
from .models import Product, Category, ProductImage, Flower


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


# Регистрация модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'discount', 'is_deal', 'get_category', 'get_flowers']
    list_filter = ['available', 'created', 'updated', 'is_deal']
    list_editable = ['price', 'available', 'discount', 'is_deal']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    search_fields = ['name', 'description']
    ordering = ['-created']

    # Добавляем возможность фильтрации по цветам
    filter_horizontal = ('flowers',)  # Это добавляет интерфейс для выбора нескольких цветов

    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = 'Категория'

    def get_flowers(self, obj):
        return ", ".join([flower.name for flower in obj.flowers.all()])
    get_flowers.short_description = 'Цветы'


# Регистрация модели Flower
@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

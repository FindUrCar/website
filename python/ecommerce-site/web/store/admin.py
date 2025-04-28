from django.contrib import admin
from .models import Product
from .utils import generate_description

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    actions = ["generate_product_description"]

    def generate_product_description(self, request, queryset):
        for product in queryset:
            if not product.description:
                product.description = generate_description(product.name)
                product.save()
        self.message_user(request, "Açıklamalar başarıyla oluşturuldu.")
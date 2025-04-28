from django.shortcuts import render,get_object_or_404
from .models import Product
import random
from .utils import search_products


# Ürünlerin listelendiği sayfa
def product_list(request):
    products = Product.objects.all()
    return render(request, "store/product_list.html", {"products": products})

# Ana sayfa, 3 rastgele ürünü çok satanlar bölümünde göster
def home_view(request):
    # Ürünlerin tamamından 3 rastgele ürün seç
    random_products = random.sample(list(Product.objects.all()), 5)  # 3 rastgele ürün seç
    
    # Home sayfasını render et, rastgele seçilen 3 ürünü gönder
    return render(request, 'store/home.html', {'random_products': random_products})

def search_view(request):
    query = request.GET.get('q', '')  # Arama sorgusunu GET parametresi olarak al
    if query:
        # Eğer sorgu varsa, ürünleri arama fonksiyonu ile ara
        products = search_products(query)
        if not products:  # Eğer hiç ürün bulunmazsa
            no_results = True  # Eşleşen ürün bulunmadığını belirt
            products = Product.objects.all()  # Tüm ürünleri göster
        else:
            no_results = False  # Ürün bulundu
    else:
        # Eğer sorgu yoksa, tüm ürünleri göster
        products = Product.objects.all()
        no_results = False

    return render(request, 'store/search_results.html', {'products': products, 'query': query, 'no_results': no_results})

def product_detail(request, product_id):
    # Ürünü ID'ye göre al
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST' and 'add_to_cart' in request.POST:
        # Sepete ekleme işlemi
        # Sepet fonksiyonelliğini burada implement edebiliriz
        pass
    
    return render(request, 'store/product_detail.html', {'product': product})
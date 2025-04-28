import requests
import json
from django.db.models import Q
from .models import Product

def generate_description(product_name):
    url = "http://llm:11434/api/generate"
    prompt = f"'{product_name}' isimli ürün için özelliklerini barındıran ama 150 kelimeyi geçmeyen bir ürün bilgisi kısmı yaz."

    response = requests.post(url, json={
        "model": "gemma3:1b",  # Daha hafif model kullanıyoruz
        "prompt": prompt,
    }, stream=True)

    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                full_response += data.get("response", "")
        print("Generated description:", full_response)
        return full_response.strip()
    else:
        print(f"Hata oluştu: {response.status_code} - {response.text}")
        return None

def search_products(query):
    # Basit metin tabanlı arama (name ve description üzerinde)
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return products    
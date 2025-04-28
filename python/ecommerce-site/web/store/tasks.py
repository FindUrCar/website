from celery import shared_task
from store.utils import generate_description
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_product_description_task(product_id):
    from store.models import Product

    try:
        product = Product.objects.get(id=product_id)
        logger.info(f"Ürün bulundu: {product.name}")

        generated_description = generate_description(product.name)

        if generated_description:
            product.description = generated_description  # ✅ Açıklamayı buraya kaydediyoruz!
            product.save()
            logger.info(f"Açıklama kaydedildi: {product.name}")
            return f"Açıklama başarıyla oluşturuldu: {product.name}"
        else:
            logger.warning(f"Açıklama üretilemedi: {product.name}")
            return f"Açıklama üretilemedi: {product.name}"

    except Product.DoesNotExist:
        logger.error(f"Ürün bulunamadı. ID: {product_id}")
        return f"Ürün bulunamadı, ID: {product_id}"

    except Exception as e:
        logger.exception(f"Beklenmeyen hata oluştu (ID: {product_id}): {str(e)}")
        return f"Hata oluştu: {str(e)}"

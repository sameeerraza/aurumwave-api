import pickle

from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Product
from utils.ai_search import load_product_embeddings, model, EMBEDDINGS_FILE_PATH


@receiver(post_save, sender=Product)
def update_product_embeddings(sender, instance, created, **kwargs):
    if created:
        products, embeddings = load_product_embeddings()

        if isinstance(products, QuerySet):
            products = list(products)

        new_product_data = f"{instance.title} {instance.description}"
        products.append(instance)
        new_embedding = model.encode([new_product_data])

        embeddings = list(embeddings) + [new_embedding.flatten()] # for surity

        with open(EMBEDDINGS_FILE_PATH, 'wb') as f:
            pickle.dump({
                'products': products,
                'embeddings': embeddings
            }, f)

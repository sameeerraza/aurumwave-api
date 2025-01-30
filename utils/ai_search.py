import os
import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from product.models import Product

# loafing a pre-trained Sentence Transformer model
model = SentenceTransformer('all-mpnet-base-v2')

EMBEDDINGS_FILE_PATH = os.path.join("assets", "product_embeddings.pkl")


def save_product_embeddings():
    if os.path.exists(EMBEDDINGS_FILE_PATH):
        print("Product already embeddings saved.")
        return

    products = Product.objects.all()

    # creatitng a list of combined strings for embedding (title + description)
    product_data = [f"{product.title} {product.description}" for product in products]

    product_embeddings = model.encode(product_data)

    with open(EMBEDDINGS_FILE_PATH, 'wb') as f:
        pickle.dump({
            'products': products,
            'embeddings': product_embeddings
        }, f)


def load_product_embeddings():
    # if the embeddings file exists
    if os.path.exists(EMBEDDINGS_FILE_PATH):
        with open(EMBEDDINGS_FILE_PATH, 'rb') as f:
            data = pickle.load(f)
        return data['products'], data['embeddings']
    return [], []


# will be called on startup
save_product_embeddings()


def advance_search(query):
    products, embeddings = load_product_embeddings()

    if not products:
        return []

    query_embedding = model.encode([query])

    # cosine similarity between the giben search query and product embeddings
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    threshold = 0.0  # vcould just fitler but osrting is better
    similar_products = []

    for idx, sim in enumerate(similarities):
        if sim >= threshold:
            similar_products.append({
                "product": products[idx],
                "similarity": sim
            })

    sorted_products = sorted(similar_products, key=lambda x: x['similarity'], reverse=True)

    return [product["product"] for product in sorted_products]

# import pandas as pd
import os

def product_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/static/products/<filename>
    return "{0}/{1}/{2}".format(
        "static", "products", filename
    )

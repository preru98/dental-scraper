from dental.integrations.redis_client import redis_cli


def update_products(product_list=[]):
    create_new_results = []
    deleted = []
    for product in product_list:
        product_name_key = product.get("product_name")
        if redis_cli.exists(product_name_key):
            product_details = redis_cli.get(product_name_key)
            if product_details.get("product_price") != product.get("product_price"):
                redis_cli.set(product_name_key, product)
                create_new_results.append(product)
                deleted.append(product_name_key)
        else:
            redis_cli.set(product_name_key, product)
            create_new_results.append(product)
    return create_new_results, deleted

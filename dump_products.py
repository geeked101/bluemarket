from cassandra.cluster import Cluster
from cassandra.query import dict_factory

try:
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('ecommerce')
    session.row_factory = dict_factory
    
    rows = session.execute("SELECT * FROM products")
    products = list(rows)
    print(f"Total products in DB: {len(products)}")
    for p in products:
        print(f"- {p['name']} (Price: {p['price']}, Image: {p['image_url']})")
    
    cluster.shutdown()
except Exception as e:
    print(f"Error: {e}")

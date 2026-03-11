from cassandra.cluster import Cluster
from cassandra.query import dict_factory

import time

def get_session():
    max_retries = 5
    for i in range(max_retries):
        try:
            # Connect to Cassandra
            cluster = Cluster(['127.0.0.1'], port=9042)
            session = cluster.connect()
            
            # Create keyspace if it doesn’t exist
            session.execute("""
                CREATE KEYSPACE IF NOT EXISTS ecommerce
                WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
            """)
            
            session.set_keyspace('ecommerce')
            session.row_factory = dict_factory
            
            # Create tables...
            # (Keeping the table creation logic inside for simplicity)
            session.execute("CREATE TABLE IF NOT EXISTS products (id uuid PRIMARY KEY, name text, description text, price decimal, stock int, image_url text, category text, rating float, review_count int, verified_seller boolean, created_at timestamp)")
            session.execute("CREATE TABLE IF NOT EXISTS users (id uuid PRIMARY KEY, username text, email text, password_hash text)")
            session.execute("CREATE INDEX IF NOT EXISTS ON users (email)")
            session.execute("CREATE TABLE IF NOT EXISTS carts (user_id uuid PRIMARY KEY, items list<uuid>)")
            session.execute("CREATE TABLE IF NOT EXISTS orders (id uuid PRIMARY KEY, user_id uuid, items list<uuid>, total decimal, delivery_fee decimal, shipping_info text, payment_method text, payment_status text, created_at timestamp)")
            
            print(f"Connected to Cassandra (Attempt {i+1})")
            return session
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                with open("backend_error.log", "a") as f:
                    f.write(f"Final failure connecting to Cassandra: {e}\n")
                return None

session = get_session()


import os
import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

def get_session():
    max_retries = 3
    
    # Environment variables for Astra DB (Production)
    bundle_path = os.environ.get('ASTRA_DB_SECURE_BUNDLE_PATH')
    client_id = os.environ.get('ASTRA_DB_CLIENT_ID')
    client_secret = os.environ.get('ASTRA_DB_CLIENT_SECRET')
    
    for i in range(max_retries):
        try:
            if bundle_path and client_id and client_secret:
                print(f"Connecting to Astra DB (Attempt {i+1})...")
                # Connect to Astra DB
                cloud_config = {
                    'secure_connect_bundle': bundle_path
                }
                auth_provider = PlainTextAuthProvider(client_id, client_secret)
                cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            else:
                print(f"Connecting to Local Cassandra (Attempt {i+1})...")
                # Connect to Local Cassandra
                cluster = Cluster(['127.0.0.1'], port=9042)
            
            session = cluster.connect()
            
            # Create keyspace if it doesn’t exist (Local only usually, Astra keyspaces are pre-created)
            if not bundle_path:
                session.execute("""
                    CREATE KEYSPACE IF NOT EXISTS ecommerce
                    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
                """)
            
            session.set_keyspace('ecommerce')
            session.row_factory = dict_factory
            
            # Ensure tables exist
            session.execute("CREATE TABLE IF NOT EXISTS products (id uuid PRIMARY KEY, name text, description text, price decimal, stock int, image_url text, category text, rating float, review_count int, verified_seller boolean, created_at timestamp)")
            session.execute("CREATE TABLE IF NOT EXISTS users (id uuid PRIMARY KEY, username text, email text, password_hash text)")
            session.execute("CREATE INDEX IF NOT EXISTS ON users (email)")
            session.execute("CREATE TABLE IF NOT EXISTS carts (user_id uuid PRIMARY KEY, items list<uuid>)")
            session.execute("CREATE TABLE IF NOT EXISTS orders (id uuid PRIMARY KEY, user_id uuid, items list<uuid>, total decimal, delivery_fee decimal, shipping_info text, payment_method text, payment_status text, created_at timestamp)")
            
            print(f"Connected to Database (Attempt {i+1})")
            return session
            
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                log_file = os.path.join(os.path.dirname(__file__), "..", "backend_error.log")
                with open(log_file, "a") as f:
                    f.write(f"Final failure connecting to Database: {e}\n")
                return None

session = get_session()


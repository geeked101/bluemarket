import os
import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

def get_session():
    max_retries = 5
    for i in range(max_retries):
        try:
            print(f"Connecting to Astra DB (Attempt {i+1})...")
            
            bundle_env = os.environ.get('ASTRA_DB_SECURE_BUNDLE_PATH', 'secure-connect-blue-market.zip')
            
            # Ensure the path is absolute so the driver can always find it
            if not os.path.isabs(bundle_env):
                bundle_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), bundle_env)
            else:
                bundle_path = bundle_env
                
            cloud_config = {
                'secure_connect_bundle': bundle_path
            }
            client_id = os.environ.get('ASTRA_DB_CLIENT_ID', '')
            client_secret = os.environ.get('ASTRA_DB_CLIENT_SECRET', '')
            keyspace = os.environ.get('ASTRA_DB_KEYSPACE', 'bluemarket')
            
            auth_provider = PlainTextAuthProvider(client_id, client_secret)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect(keyspace)
            
            session.row_factory = dict_factory
            
            # Ensure tables exist
            session.execute("CREATE TABLE IF NOT EXISTS products (id uuid PRIMARY KEY, name text, description text, price decimal, stock int, image_url text, category text, rating float, review_count int, verified_seller boolean, created_at timestamp)")
            session.execute("CREATE TABLE IF NOT EXISTS users (id uuid PRIMARY KEY, username text, email text, password_hash text)")
            session.execute("CREATE INDEX IF NOT EXISTS ON users (email)")
            session.execute("CREATE TABLE IF NOT EXISTS carts (user_id uuid PRIMARY KEY, items list<uuid>)")
            session.execute("CREATE TABLE IF NOT EXISTS orders (id uuid PRIMARY KEY, user_id uuid, items list<uuid>, total decimal, delivery_fee decimal, shipping_info text, payment_method text, payment_status text, created_at timestamp)")
            
            print(f"Connected to Astra DB (Attempt {i+1})")
            return session
            
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                log_file = os.path.join(os.path.dirname(__file__), "..", "backend_error.log")
                with open(log_file, "a") as f:
                    f.write(f"Final failure connecting to Astra DB: {e}\n")
                return None

session = get_session()


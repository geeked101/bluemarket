from flask import Flask
from flask_cors import CORS
from backend.routes.products import products_bp
from backend.db import session
from backend.routes.auth import auth_bp
from backend.routes.orders import orders_bp

app = Flask(__name__)
# Enable CORS for all domains so Netlify can fetch without block
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Register Blueprints
app.register_blueprint(products_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
@app.route("/")
def home():
    return {"message": "E-commerce API running 🔥"}

if __name__ == "__main__":
    app.run(debug=True)

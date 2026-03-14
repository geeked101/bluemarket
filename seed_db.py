import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from decimal import Decimal

def seed():
    try:
        from backend.db import session
        
        if not session:
            print("Failed to get DB session")
            return

        products = [
            {
                "name": "Porsche 911 GT3",
                "description": "High-performance tactical transport. Sleek, fast, and engineered for precision.",
                "price": Decimal("18500000"),
                "image": "images/911.jpeg",
                "category": "Vehicles"
            },
            {
                "name": "Nissan GT-R R35",
                "description": "The ultimate street weapon. Twin-turbocharged performance for high-stakes maneuvers.",
                "price": Decimal("12500000"),
                "image": "images/GTR.jpeg",
                "category": "Vehicles"
            },
            {
                "name": "Tactical Operator Rifle",
                "description": "Custom-built for the modern operative. Features modular rail system and suppressive capabilities.",
                "price": Decimal("450000"),
                "image": "images/gun.jpg",
                "category": "Tactical"
            },
            {
                "name": "Sidearm Elite",
                "description": "Reliable secondary for close-quarters engagements. Ergonomic grip and enhanced sights.",
                "price": Decimal("85000"),
                "image": "images/gun2.jpeg",
                "category": "Tactical"
            },
            {
                "name": "Compact SMG",
                "description": "High rate of fire in a compact frame. Perfect for rapid response missions.",
                "price": Decimal("220000"),
                "image": "images/gun3.jpg",
                "category": "Tactical"
            },
            {
                "name": "Stealth Porsche",
                "description": "Midnight-tuned Porsche for low-visibility operations.",
                "price": Decimal("15000000"),
                "image": "images/porshe.jpg",
                "category": "Vehicles"
            },
            {
                "name": "Forest Camo Gear",
                "description": "Full-body concealment system optimized for woodland environments.",
                "price": Decimal("45000"),
                "image": "images/tree.jpg",
                "category": "Gear"
            },
            {
                "name": "Night Ops Green Vests",
                "description": "Heavy-duty protective gear with night-vision compatible finish.",
                "price": Decimal("65000"),
                "image": "images/green.jpg",
                "category": "Gear"
            },
            {
                "name": "Interceptor Red Unit",
                "description": "Rapid response tactical unit for high-visibility deterrence.",
                "price": Decimal("9500000"),
                "image": "images/red.jpg",
                "category": "Vehicles"
            }
        ]

        insert_stmt = session.prepare("""
            INSERT INTO products (id, name, description, price, stock, image_url, category, rating, review_count, verified_seller, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

        for p in products:
            session.execute(insert_stmt, (
                uuid.uuid4(),
                p['name'],
                p['description'],
                p['price'],
                10,
                p['image'],
                p['category'],
                4.8,
                12,
                True,
                datetime.now()
            ))

        print(f"Successfully seeded {len(products)} products into 'ecommerce.products'!")

    except Exception as e:
        print(f"Seeding failed: {e}")

if __name__ == "__main__":
    seed()

# Blue Market 🛡️

Blue Market is a premium, modern e-commerce platform designed with a sleek "tactical" aesthetic. It provides a seamless shopping experience for digital assets, tactical gear, or any curated catalog, featuring a robust Flask backend and an Apache Cassandra database for high availability and scalability.

## ✨ Features

- **Premium UI/UX**: Dark-themed, responsive design with glassmorphism and smooth transitions.
- **Dynamic Asset Catalog**: Real-time filtering, searching, and sorting of products.
- **Secure Authentication**: JWT-based auth with salted password hashing (Bcrypt).
- **Persistent Cart**: Client-side cart management using local storage.
- **Scalable Database**: Powered by Apache Cassandra for high-performance data handling.
- **Verified Sellers**: Badging system for trusted merchants.

---

## 🚀 Tech Stack

### Frontend
- **HTML5 & CSS3**: Custom design system using CSS variables, flexbox, and grid.
- **Vanilla JavaScript**: Pure ES6+ logic for handling API interactions and DOM manipulation.
- **Animations**: Subtle micro-animations for an interactive feel.

### Backend
- **Python / Flask**: Restful API for handling business logic and data routing.
- **JWT (JSON Web Tokens)**: Secure stateless authentication.
- **Bcrypt**: Industrial-grade password hashing.
- **Flask-CORS**: Cross-Origin Resource Sharing for frontend-backend communication.

### Database
- **Apache Cassandra**: Distributed NoSQL database for flexible and scalable data models.

---

## 🛠️ Getting Started

Follow these steps to set up the project locally.

### 1. Prerequisites
- **Python 3.8+**
- **Apache Cassandra** (Running locally on port `9042`)
- **Web Browser** (Chrome, Firefox, or Brave recommended)

### 2. Database Setup
Ensure Cassandra is running:
```powershell
# On Windows (if installed as a service)
Start-Service "DataStax Cassandra Community Server"
```
The backend is configured to automatically create the `ecommerce` keyspace and all necessary tables (`users`, `products`, `carts`, `orders`) on its first run.

### 3. Backend Installation
1. Start from the project root (`Blue market/`).
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Start the Flask server (from the root directory):
   ```bash
   python -m backend.app
   ```
   The API will be available at `http://localhost:5000`.


### 4. Frontend Setup
Simply open the `index.html` file in your browser:
- Locate `frontend/index.html` and double-click it.
- **OR** use a local server (like Live Server in VS Code) for a better experience.

---

## 📂 Project Structure

```text
Blue market/
├── backend/            # Flask API
│   ├── routes/         # API Endpoints (Auth, Products, Orders)
│   ├── app.py          # Main Entry Point
│   ├── db.py           # Database Connection & Schema
│   └── requirements.txt
└── frontend/           # Vanilla Web Client
    ├── css/            # Stylesheets
    ├── js/             # Application Logic
    ├── images/         # Static Assets
    └── *.html          # UI Pages
```

## 🔐 Security Note
The current setup uses a default Cassandra configuration (`127.0.0.1:9042`). For production environments, ensure you update the cluster connection settings in `backend/db.py` and use environment variables for secret keys.

---
*Created with focus on performance and aesthetics.*

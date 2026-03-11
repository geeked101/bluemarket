import requests
try:
    res = requests.post("http://localhost:5000/api/auth/login", json={"email": "test@example.com", "password": "password"})
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(("127.0.0.1", 9042))
    print("Socket connected to 127.0.0.1:9042")
except Exception as e:
    print(f"Failed to connect to 127.0.0.1: {e}")
finally:
    s.close()

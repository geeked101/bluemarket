from cassandra.cluster import Cluster
try:
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    print("Success!")
    cluster.shutdown()
except Exception as e:
    print(f"Failed: {e}")

from pymilvus import connections, db


def start_milvus_db():
    connections.connect(host="localhost", port="19530")
    database = db.create_database("llama_fast")

print(db.list_database())

if __name__ == "__main__":
    start_milvus_db()

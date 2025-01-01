import pickle
import time
import create
import base64

def create_db_header(name):
    header = {
        "db_name": name,
        "version": 1,
        "num_tables": 0,
        "creation_time": str(time.time())
    }
    binary_data = pickle.dumps(header)

    text_data = base64.b64encode(binary_data).decode('utf-8')

    print(binary_data)
    print(pickle.loads(binary_data))
    
def create_table(query):
    info = create.parse_create_table(query)
    data = pickle.dumps(info)
    print(data)
    print(pickle.loads(data))


query = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


create_db_header("Hello World")
create_table(query)

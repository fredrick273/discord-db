import pickle
import time
import create
import base64
import sqlparse
import os

from dotenv import load_dotenv
load_dotenv()
GUILD = int(os.getenv('GUILD'))

def get_dbinfo_channel(client):
    channels = client.get_guild(GUILD).text_channels
    for i in channels:
        if i.name == 'dbinfo':
            return i
    return None


async def process_query(query, client):
    """Process an SQL query and handle database or table creation."""
    parsed = sqlparse.parse(query)[0]
    tokens = [token for token in parsed.tokens if not token.is_whitespace]

    if parsed.get_type() == "CREATE":
        if tokens[1].value.upper() == "DATABASE":
            info, db_name = create_db_header(query)

            for channel in client.get_guild(GUILD).channels:
                await channel.delete()
            
            await client.get_guild(GUILD).create_text_channel("dbinfo")

            dbinfo_channel = get_dbinfo_channel(client)
            if dbinfo_channel:

                await client.get_channel(dbinfo_channel.id).send(info)
                print(f"Created database successfully: {db_name}")
            else:
                print("Error: 'dbinfo' channel not found.")
        elif tokens[1].value.upper() == "TABLE":
            table_info = create_table(query)
            print(f"Table created successfully: {table_info}")
        else:
            print("Unsupported CREATE statement.")
    else:
        print("No other query type supported as of now.")


def create_db_header(query):
    info = create.parse_create_db(query)

    header = {
        "db_name": info['db_name'],
        "version": 1,
        "num_tables": 0,
        "creation_time": str(time.time())
    }
    binary_data = pickle.dumps(header)
    text_data = base64.b64encode(binary_data).decode('utf-8')
    return text_data,info["db_name"]
    
def create_table(query):
    info = create.parse_create_table(query)
    data = pickle.dumps(info)
    print(data)
    print(pickle.loads(data))


# query = """
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     username TEXT NOT NULL UNIQUE,
#     email TEXT UNIQUE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """


# create_db_header("Hello World")
# create_table(query)

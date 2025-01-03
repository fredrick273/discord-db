
import sqlparse
import json

def parse_create_table(query):
    parsed = sqlparse.parse(query)[0]
    tokens = [token for token in parsed.tokens if not token.is_whitespace]
    
    table_info = {"table_name": None, "columns": []}
    
    if parsed.get_type() == "CREATE":
        if tokens[1].value.upper() == "TABLE":
            table_info["table_name"] = tokens[2].get_name()
    
    parenthesis = next(token for token in tokens if token.value.startswith("("))
    columns_definition = parenthesis.value.strip("()").split(",")
    
    for column_def in columns_definition:
        column_parts = column_def.strip().split()
        column_name = column_parts[0]
        column_type = column_parts[1]
        
        constraints = []
        for part in column_parts[2:]:
            if part.upper() in {"PRIMARY", "NOT", "UNIQUE", "DEFAULT"}:
                constraints.append(part)
        
        table_info["columns"].append({
            "name": column_name,
            "type": column_type,
            "constraints": constraints
        })
    
    return table_info

def parse_create_db(query):
    parsed = sqlparse.parse(query)[0]  
    tokens = [token for token in parsed.tokens if not token.is_whitespace]
    info = {"db_name": None}
    if parsed.get_type() == "CREATE" and tokens[1].value.upper() == "DATABASE":
        info['db_name'] = tokens[2].value  

    return info
    

# Example usage

if __name__ == '__main__':
    query = """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    result = parse_create_table(query)
    print(json.dumps(result, indent=1))
    print(parse_create_db("CREATE DATABASE databasename;"))

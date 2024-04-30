import json

with open('./spider/tables.json', 'r') as file:
    databases  = json.load(file)

def find_database_by_id(databases, db_id):
    for db in databases:
        if db["db_id"] == db_id:
            return db
    return None  


def format_schema_for_model(database, question):
    db_id = database["db_id"]
    tables_columns = ""
    for index, table_name in enumerate(database["table_names_original"]):
        columns = [col[1] for col in database["column_names_original"] if col[0] == index]
        columns_formatted = ", ".join(columns)
        tables_columns += f"{table_name} : {columns_formatted} | "
    return f"{question} | {db_id} | {tables_columns[:-2]}"

def generate_querry(question,target_db_id):
    return format_schema_for_model(find_database_by_id(databases, target_db_id),question)


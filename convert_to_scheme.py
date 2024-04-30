#tento skript převádí schéma tabulek z create table příkazu na schéma typu:
# [table] : [column] ( [content] , [content] ) , [column] ( ... ) , [...] | [table] : ... | ...
#
#
#

import re

def loadTable(table_name):
    f =open("spider/database/"+table_name+"/schema.sql",'r')
    create_table_commands = ""
    lines=f.read()
    commands = lines.split(";")

    for command in commands:
        if command.strip().startswith("CREATE TABLE"):
            create_table_commands+=(command.strip() + ";\n")
        if command.strip().startswith("create table"):
            create_table_commands+=(command.strip() + ";\n")

    f.close()
    return create_table_commands


class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []
        self.types = []
        self.keys = []

    def add_column(self, column_name, column_type, key_info=None):
        self.columns.append(column_name)
        self.types.append(column_type)
        self.keys.append(key_info or '')

    def ToString(self):
        name =self.name.strip()
        result=name+" :"
        for c, t,k in zip(self.columns,self.types,self.keys):
            #print(k)
            c=c.strip()
            t=t.strip()
            k=k.strip()
            result+=" "+c+" " #column name
            if k == '': #if row is not pk or fk
                result+=f"( {t} )"
            else:
                result+=f"( {t} , {k} )"
            result+=' , '
        result =re.sub(r',([^,]*)$', r'\1', result) #last ','
        return result

def parse_sql_file(sql_text):
    tables = []
    table_creates = re.findall(r'create table\s+(\w+)\s*\((.*?)\)\s*;', sql_text, re.DOTALL)

    for table_name, table_body in table_creates:
        current_table = Table(table_name)

        columns_part = table_body.split('constrain')[0]
        column_definitions = re.findall(r'(\w+)\s+(\w+)(\([^\)]*\))?\s*([^,]*)', columns_part)

        for column_def in column_definitions:
            column_name, column_type, _, key_part = column_def
            key_info = None
            if 'primary key' in key_part:
                key_info = 'PRIMARY KEY'
            if column_name not in ["not", "null","primary","foreign"] and column_type not in ["not", "null","primary","foreign"]:
                current_table.add_column(column_name, column_type, key_info)

        #primary_keys = re.search(r'PRIMARY KEY\s*\(([^)]+)\)', table_body)
        primary_keys = re.search(r'primary key\s*\(([^)]+)\)', table_body)
        if primary_keys:
            pk_columns = [x.strip() for x in primary_keys.group(1).split(',')]
            for pk in pk_columns:
                for i, column in enumerate(current_table.columns):
                    if column == pk:
                        current_table.keys[i] = 'PRIMARY KEY'

        #foreign_keys = re.findall(r'FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*(\w+)\s*\(([^)]+)\)', table_body)
        foreign_keys = re.findall(r'foreign key\s*\(([^)]+)\)\s*references\s*(\w+)\s*\(([^)]+)\)', table_body)
        for fk in foreign_keys:
            fk_column, ref_table, ref_column = fk[0].strip(), fk[1], fk[2]
            for i, column in enumerate(current_table.columns):
                if column == fk_column:
                    current_table.keys[i] = f'FOREIGN KEY ({ref_table}.{ref_column})'

        tables.append(current_table)

    return tables


def adjust_brackets(sql_text):
    adjusted_text = re.sub(r'(CREATE|create)\s+([^\n]*?)\(', r'\1 \2\n(', sql_text)
    return adjusted_text


def convert_sql_to_scheme(sql): ##<-----------------------
    result=""
    sql=sql.replace("\t"," ")
    sql=sql.replace("       ","")
    sql=sql.lower()
    sql=sql.replace("'","")
    sql=sql.replace("`","")
    #print("sql")###
    #print(sql)###
    tables=parse_sql_file(adjust_brackets(sql.replace('"','')))
    for t in tables:
        result+=t.ToString().strip()+' | '
    result =re.sub(r'\|([^|]*)$', r'\1', result)  #last '|'
    return result

def generate_querry(question,target_db_id):
    sql =loadTable(target_db_id)
    scheme =convert_sql_to_scheme(sql)
    return (f"{question} | {target_db_id} | {scheme}") 

from sqlalchemy import create_engine
import pandas as pd

class ConnectSQL():
    def __init__(self, db_data):
        self.conn = self.__create_connection(db_data)
        return

    #Gibt Connection zum Datenbank aus
    def __create_connection(self, db_data):
        try:
            engine = create_engine("{rdbms}://{user}:{passwd}@{host}/{db}".format(rdbms = db_data["rdbms_name"], user = db_data["user_name"], passwd = db_data["password"], host = db_data["host_name"], db = db_data["database_name"]))
            connection = engine.connect()
            return connection
        except:
            print("ConnectSQL: Error while connecting to database")

    #Erstellt Tabelle aus einem pd.DataFrame
    def create_table(self, dataframe: pd.DataFrame, table_name: str):
        dataframe.to_sql(table_name, self.conn, if_exists="replace")

    #Macht index_id Spalte zum PRIMARY KEY
    def add_primary_key_as_index(self, table_name: str):
        try:
            self.conn.execute("ALTER TABLE {0} ADD PRIMARY KEY(index_id);".format(table_name))
        except:
            print("ConnectSQL: Error while adding primary key in table {0}".format(table_name))

    #Macht index_id's der anderen Tabellen zum FOREIGN KEY. Dabei sollen die index_id Spalten in eigenen Tabellen PRIMARY KEY sein
    def add_foreign_key_as_index(self, table_name_1, table_name_2, column_name):
        try:
            self.conn.execute("ALTER TABLE {0} ADD FOREIGN KEY({1}) REFERENCES {2}(index_id)".format(table_name_1, column_name, table_name_2))
        except:
            print("ConnectSQL: Error while adding foreign key in table {0} references table {1}".format(table_name_1, table_name_2))

    #aendert den Typ der in angegebenen Spalten erhaltenen Values
    def modify_column_type_in_table(self, table_name, column_name, type: str):
        try:
            self.conn.execute("ALTER TABLE {0} MODIFY {1} {2}".format(table_name, column_name, type))
        except:
            print("ConnectSQL: Error while modifying column type")
import pandas as pd
from sql_db_connect import ConnectSQL

class JSONtoSQL():
    def __init__(self, json_file: str, sql_db_data: dict, main_table_name: str, rows_num: int = 0):
        self.json_file = json_file
        self.sql_db_data = sql_db_data
        self.main_table_name = main_table_name
        self.rows_num = rows_num

    def json_to_sql(self):
        #Ermittlung der Haupttabelle
        if self.rows_num != 0:
            data = pd.read_json(self.json_file, lines=True).head(self.rows_num)
        elif self.rows_num == 0:
            data = pd.read_json(self.json_file, lines=True)
        #obwohl in manche Tabellen es schon IDs gibt, werden hier neue generiert, um den Prozess zu verallgemeinern
        data.index.name = "index_id"
        #Dictionaries, die in Spalten der Haupttabelle stehen, werden in pd.DataFrame's umgewandelt
        dict_columns = self.__get_names_of_columns_with_type(data, dict)
        dict_columns_values = self.__get_dict_column_values(data, dict_columns)
        secondary_dataframes = self.__create_dataframes(dict_columns, dict_columns_values)

        #Dictionaries, die in Spalten der Haupttabelle stehen, werden durh ihre index_id's ersetzt
        for name in dict_columns:
            data = self.__dict_columns_to_index_columns(data, name, secondary_dataframes[name])

        print("First stage complete: data transformation")

        #Connection zum SQL Datenbank
        connectSQL = ConnectSQL(self.sql_db_data)

        #Erstellung von Tabellen im Datenbank und aenderung der Spalten. Es werden index_id's in jeder Tabelle zu PRIMARY KEY gemacht
        #und in der Haupttabelle bestimmte Spalten zum FOREIGN KEY gemacht.
        connectSQL.create_table(data, self.main_table_name)
        connectSQL.modify_column_type_in_table(self.main_table_name, "index_id", "INT UNSIGNED")
        connectSQL.add_primary_key_as_index(self.main_table_name)
        for name in dict_columns:
            connectSQL.create_table(secondary_dataframes[name], name)
            connectSQL.modify_column_type_in_table(name, "index_id", "INT UNSIGNED")
            connectSQL.add_primary_key_as_index(name)

        for name in dict_columns:
            connectSQL.modify_column_type_in_table(self.main_table_name, name, "INT UNSIGNED")
            connectSQL.add_foreign_key_as_index(self.main_table_name, name, name)

        print("Second stage complete: sent to sql db")

    #Gibt Namen der Spalten, die Dictionaries erhalten, aus
    def __get_names_of_columns_with_type(self, d: pd.DataFrame, data_type):
        dict_columns = []
        for col in d.columns:
            for i in d[col]:
                if type(i) != data_type and type(i) == type(i):
                    break
                elif type(i) == data_type:
                    dict_columns.append(col)
                    break
        return dict_columns

    #Gibt Dictionaries, die in Spalten der Haupttabelle erhalten sind, aus
    def __get_dict_column_values(self, d, dict_columns):
        dict_columns_values = {}
        for col in dict_columns:
            values = []
            for i in range(len(d[col])):
                values.append(d[col][i])
            dict_columns_values["{0}".format(col)] = values
        return dict_columns_values

    #Gibt Keys der Dictionaries und Values jeder einzelnen Dictionary aus
    def __get_vals_and_keys(self, series):
        keys = None
        vals = []
        for i in series:
            if type(i) == type(i):
                keys = list(i.keys())
                break
        for i in series:
            if i != i:
                a = []
                for j in range(0, len(keys)):
                    a.append("NULL")
                vals.append(a)
            else:
                vals.append(list(i.values()))

        return [keys, vals]

    #Erstellt pd.Dataframes aus bevor erhaltene Values und Keys
    def __create_dataframes(self, dict_columns, dict_columns_values):
        dataframes = {}
        for name in dict_columns:
            d = self.__get_vals_and_keys(dict_columns_values["{0}".format(name)])
            dataframes["{0}".format(name)] = pd.DataFrame(d[1], columns = d[0])
            dataframes["{0}".format(name)].index.name = "index_id"
        return dataframes

    #Ersatz der Values in Spalten in der Haupttabelle, die Dictionaries erhalten, durch index_id's der Tabllen, 
    #die aus der Dictionaries gemacht wurden
    def __dict_columns_to_index_columns(self, main_df, column_name, secondary_df):
        main_df[column_name] = main_df[column_name].replace(list(main_df[column_name]), secondary_df.index)
        return main_df
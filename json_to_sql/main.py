from json_to_sql import JSONtoSQL

#Data fuer Zugriff zum mysql Datenbank
sql_db_data = {"rdbms_name":"mysql", "user_name":"root", "host_name":"127.0.0.1", "password":"qaz4567plm", "database_name":"italian_music_db"}

#Transportierung der json File zum Datenbank
trans = JSONtoSQL("datasets/the_italian_music_dataset.json", sql_db_data, "songs", 20)
trans.json_to_sql()
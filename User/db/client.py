from pymongo import MongoClient

# Nos creamos un objeto de tipo MongoClient
# Al crear el objeto ya establecemos una conexión con la base de datos
# No le indicamos ningún parámetro al constructor porque tenemos 
# la base de datos en local. 
# Si la base de datos estuviese en un servidor sí que tendríamos 
# que indicar los datos de conexión

# Base de datos en local
# db_client = MongoClient()


# Base de datos en remoto
db_client = MongoClient("mongodb+srv://elenarivero_db_user:1234@cluster0.xu7oyb3.mongodb.net/?appName=Cluster0")




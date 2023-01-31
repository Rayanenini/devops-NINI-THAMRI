import psycopg2

# Paramètres de connexion à la base de données
conn = psycopg2.connect(
    host="127.0.0.1",
    database="db",
    user="usr",
    password="pwd"
)

# Création d'un curseur pour exécuter des requêtes
cursor = conn.cursor()

# Exécution d'une requête SQL
"""cursor.execute("CREATE TABLE public.departments (id SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL);")
cursor.execute("INSERT INTO departments (name) VALUES ('IRC');")"""
cursor.execute("SELECT * FROM public.departments")

# Récupération des résultats de la requête
rows = cursor.fetchall()

# Boucle sur les lignes du résultat
for row in rows:
    print(row)

# Fermeture de la connexion à la base de données
conn.close()

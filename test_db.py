import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reservation_sportive"
    )
    print("✅ Connexion réussie à la base de données !")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Erreur de connexion : {err}")

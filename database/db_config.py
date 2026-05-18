import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@IpshitaSri06",
    database="flowpilot"
)

cursor = db.cursor()

print("Database Connected Successfully")
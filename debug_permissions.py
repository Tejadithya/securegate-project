import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="teja@2004",
    database="progres"
)
cursor = conn.cursor()

print("\n=== ROLES ===")
cursor.execute("SELECT id, name FROM roles ORDER BY id")
for row in cursor.fetchall():
    print(row)

print("\n=== USERS ===")
cursor.execute("SELECT id, username FROM users ORDER BY id")
for row in cursor.fetchall():
    print(row)

print("\n=== USER ROLES ===")
cursor.execute("""
    SELECT u.id, u.username, r.id, r.name 
    FROM users u 
    LEFT JOIN user_roles ur ON u.id = ur.user_id 
    LEFT JOIN roles r ON ur.role_id = r.id 
    ORDER BY u.id
""")
for row in cursor.fetchall():
    print(row)

print("\n=== PERMISSIONS ===")
cursor.execute("SELECT id, name FROM permissions ORDER BY id")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()

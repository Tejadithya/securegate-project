import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL (default postgres database)
try:
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="teja@2004",
        database="postgres"
    )
    conn.autocommit = True  # Required for CREATE DATABASE
    cursor = conn.cursor()
    
    # Check if progres database exists
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
        ("progres",)
    )
    exists = cursor.fetchone()
    
    if not exists:
        print("Creating database 'progres'...")
        cursor.execute(sql.SQL("CREATE DATABASE progres"))
        print("✓ Database 'progres' created successfully")
    else:
        print("✓ Database 'progres' already exists")
    
    cursor.close()
    conn.close()
    
    # Now create tables and seed data
    conn2 = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="teja@2004",
        database="progres"
    )
    cursor2 = conn2.cursor()
    
    # Create users table
    cursor2.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    
    # Create roles table
    cursor2.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        )
    """)
    
    # Create permissions table
    cursor2.execute("""
        CREATE TABLE IF NOT EXISTS permissions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        )
    """)
    
    # Create user_roles junction table
    cursor2.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER REFERENCES users(id),
            role_id INTEGER REFERENCES roles(id),
            PRIMARY KEY (user_id, role_id)
        )
    """)
    
    # Create role_permissions junction table
    cursor2.execute("""
        CREATE TABLE IF NOT EXISTS role_permissions (
            role_id INTEGER REFERENCES roles(id),
            permission_id INTEGER REFERENCES permissions(id),
            PRIMARY KEY (role_id, permission_id)
        )
    """)
    
    # Clear existing data (fresh setup)
    cursor2.execute("DELETE FROM user_roles")
    cursor2.execute("DELETE FROM role_permissions")
    cursor2.execute("DELETE FROM users")
    cursor2.execute("DELETE FROM roles")
    cursor2.execute("DELETE FROM permissions")
    
    # Insert permissions
    permissions = [("READ_DATA",), ("WRITE_DATA",), ("ADMIN",)]
    for perm in permissions:
        cursor2.execute("""
            INSERT INTO permissions (name) VALUES (%s)
        """, perm)
    
    # Insert roles
    roles = [("Admin",), ("User",)]
    for role in roles:
        cursor2.execute("""
            INSERT INTO roles (name) VALUES (%s)
        """, role)
    
    # Get permission IDs
    cursor2.execute("SELECT id, name FROM permissions")
    perms = {row[1]: row[0] for row in cursor2.fetchall()}
    
    # Get role IDs
    cursor2.execute("SELECT id, name FROM roles")
    roles_dict = {row[1]: row[0] for row in cursor2.fetchall()}
    
    # Assign permissions to roles
    # Admin gets all permissions
    for perm_name in ["READ_DATA", "WRITE_DATA", "ADMIN"]:
        cursor2.execute("""
            INSERT INTO role_permissions (role_id, permission_id)
            VALUES (%s, %s)
        """, (roles_dict["Admin"], perms[perm_name]))
    
    # User gets only READ_DATA
    cursor2.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        VALUES (%s, %s)
    """, (roles_dict["User"], perms["READ_DATA"]))
    
    # Insert test users
    cursor2.execute("""
        INSERT INTO users (username, password) 
        VALUES (%s, %s)
    """, ("admin", "admin123"))
    
    cursor2.execute("""
        INSERT INTO users (username, password) 
        VALUES (%s, %s)
    """, ("user", "user123"))
    
    # Get user IDs
    cursor2.execute("SELECT id, username FROM users")
    users_dict = {row[1]: row[0] for row in cursor2.fetchall()}
    
    # Assign Admin role to admin user
    cursor2.execute("""
        INSERT INTO user_roles (user_id, role_id)
        VALUES (%s, %s)
    """, (users_dict["admin"], roles_dict["Admin"]))
    
    # Assign User role to regular user
    cursor2.execute("""
        INSERT INTO user_roles (user_id, role_id)
        VALUES (%s, %s)
    """, (users_dict["user"], roles_dict["User"]))
    
    conn2.commit()
    print("✓ Database tables created successfully")
    print("✓ Permissions created: READ_DATA, WRITE_DATA, ADMIN")
    print("✓ Roles created: Admin, User")
    print("✓ Test users created:")
    print("  - admin user (password: admin123) with Admin role and all permissions")
    print("  - user user (password: user123) with User role and READ_DATA permission")
    
    cursor2.close()
    conn2.close()
    
except Exception as e:
    print(f"Error: {e}")


# auth.py
import bcrypt
import snowflake.connector
from config import SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, SNOWFLAKE_WAREHOUSE

# Hardcoded Admin Emails
ADMIN_EMAILS = {"admin1@example.com", "admin2@example.com"}

# Connect to Snowflake
def get_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

# Hash Password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Verify Password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Register User
def register_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT email FROM users WHERE email = %s;", (email,))
    if cur.fetchone():
        return "⚠️ User already exists!"

    hashed_pw = hash_password(password)
    role = "admin" if email in ADMIN_EMAILS else "user"  # Assign role based on email

    cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s);", 
                (name, email, hashed_pw, role))
    conn.commit()

    cur.close()
    conn.close()
    return "✅ Registration successful!"

# Login User
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_id, password, role FROM users WHERE email = %s;", (email,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and verify_password(password, user[1]):
        return {"user_id": user[0], "role": user[2]}
    else:
        return None


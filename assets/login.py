from sqlalchemy import create_engine, MetaData, Table, select

from assets.logingtime import logtime

# MySQL Database URI
DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"

# Initialize SQLAlchemy engine
try:
    engine = create_engine(DATABASE_URI)
    metadata = MetaData()
    users_table = Table('login', metadata, autoload_with=engine)
except Exception as e:
    print(f"Database connection error: {e}")
    raise

# Fetch credentials from MySQL
# Fetch valid credentials from MySQL for BasicAuth
@logtime
def get_valid_credentials():
    try:
        with engine.connect() as connection:
            # Updated select syntax for SQLAlchemy 2.0+
            query = select(users_table.c.username, users_table.c.password)
            result = connection.execute(query).fetchall()
            print(result)
            return {row[0]: row[1] for row in result}
    except Exception as e:
        print(f"Error fetching credentials: {e}")
        return {}

@logtime
def verify_credentials(username, password):
    try:
        with engine.connect() as connection:
            query = select(users_table).where(
                (users_table.c.username == username) & 
                (users_table.c.password == password)
            )
            print("Executing query:", query)  # Debug
            result = connection.execute(query).fetchone()
            print("Query result:", result)    # Debug
            if result:
                return {"username": result['username'], "role": result['role']}
            return None
    except Exception as e:
        print(f"Error verifying credentials: {e}")
        return None
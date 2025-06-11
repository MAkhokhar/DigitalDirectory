from sqlalchemy import create_engine, MetaData, Table, select, insert
import pandas as pd

DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"
engine = create_engine(DATABASE_URI)
metadata = MetaData()

def fetch_contacts():
    try:
        contacts_table = Table('rsucontacts', metadata, autoload_with=engine)
        with engine.connect() as connection:
            query = select(contacts_table)
            result = connection.execute(query)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return pd.DataFrame()

def fetch_lsucontacts():
    try:
        contacts_table = Table('contacts_1', metadata, autoload_with=engine)
        with engine.connect() as connection:
            query = select(contacts_table)
            result = connection.execute(query)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return pd.DataFrame()
    
def insert_contact(new_entry):
    try:
        # Reflect the existing table
        contacts_table = Table('rsucontacts', metadata, autoload_with=engine)
        
        # Create insert statement
        stmt = insert(contacts_table).values(**new_entry)
        
        # Execute the transaction
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                result = connection.execute(stmt)
                transaction.commit()
                print(f"Inserted contact ID: {result.inserted_primary_key[0]}")
                return True
            except Exception as e:
                transaction.rollback()
                print(f"Insert failed: {str(e)}")
                return False
                
    except Exception as e:
        print(f"Database error: {str(e)}")
        return False
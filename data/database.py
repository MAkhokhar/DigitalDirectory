from sqlalchemy import create_engine, MetaData, Table, select, text, insert
import pandas as pd
import logging

DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"
engine = create_engine(DATABASE_URI)
metadata = MetaData()
rsucontacts_table = Table('rsucontacts', metadata, autoload_with=engine)

def load_data_from_db():
    with engine.connect() as connection:
        query = "SELECT * FROM rsucontacts"
        df = pd.read_sql(query, connection)
    return df

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
        contacts_table = Table('contacts_2', metadata, autoload_with=engine)
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
        stmt = engine.insert(contacts_table).values(**new_entry)
        
        # Execute the transaction
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                result = connection.execute(stmt)
                transaction.commit()
                return True, f"Contact inserted successfully! ID: {result.inserted_primary_key[0]}"
            except Exception as e:
                transaction.rollback()
                return False, f"Insert failed: {str(e)}"
                
    except Exception as e:
        return False, f"Database error: {str(e)}"
    



def add_contact_to_db2(contact_data):
    """
    Insert a new contact into the rsucontacts table
    Handles the specific data structure provided
    """
    try:
        # Map the input fields to database columns
        mapped_data = {
            'name': f"{contact_data.get('First Name', '')} {contact_data.get('Middle Name', '')} {contact_data.get('Last Name', '')}".strip(),
            'gender': contact_data.get('Gender'),
            'email': contact_data.get('Email'),
            'cellno': contact_data.get('Cell No'),
            'department': contact_data.get('Department'),
            'position': contact_data.get('Designation'),
            'address': contact_data.get('Postal Address'),
            'district': contact_data.get('District'),
            'cnic': contact_data.get('CNIC'),
            'organisation': contact_data.get('Organisation'),
            'union_council': contact_data.get('Union Council'),
            'tehsil': contact_data.get('Tehsil')
        }
        
        # Filter out None values
        db_data = {k: v for k, v in mapped_data.items() if v is not None}
        
        # Execute SQL insertion
        with engine.connect() as conn:
            stmt = text("""
                INSERT INTO rsucontacts 
                (name, gender, email, cellno, department, position, 
                 address, district, cnic, organisation, union_council, tehsil)
                VALUES 
                (:name, :gender, :email, :cellno, :department, :position, 
                 :address, :district, :cnic, :organisation, :union_council, :tehsil)
            """)
            conn.execute(stmt, db_data)
            conn.commit()
        
        return True, "Contact added successfully!"
    except Exception as e:
        return False, f"Database error: {str(e)}"


def add_contact_to_db(contact_data):
    """
    Insert a new contact into the rsucontacts table
    using the exact column names from your database
    """
    try:
        # Combine name parts
        first_name = contact_data.get('First Name', '')
        middle_name = contact_data.get('Middle Name', '')
        last_name = contact_data.get('Last Name', '')
        
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        
        # Prepare data dictionary with exact column names
        db_data = {
            "Name": full_name,
            "Gender": contact_data.get('Gender'),
            "Designation": contact_data.get('Designation'),
            "Organisation": contact_data.get('Organisation'),
            "Department": contact_data.get('Department'),
            "Group": contact_data.get('Group'),
            "Email": contact_data.get('Email'),
            "Cell No": contact_data.get('Cell No'),
            "Home phone No": contact_data.get('Home phone No'),
            "Landline / Fax": contact_data.get('Landline / Fax'),
            "CNIC": contact_data.get('CNIC'),
            "Postal Address": contact_data.get('Postal Address'),
            "Union Council": contact_data.get('Union Council'),
            "District": contact_data.get('District'),
            "Tehsil": contact_data.get('Tehsil')
        }
        
        # Filter out None values (use NULL in database)
        db_data = {k: v for k, v in db_data.items() if v is not None}
        
        # Generate SQL query
        columns = ", ".join(db_data.keys())
        placeholders = ", ".join([f":{key}" for key in db_data.keys()])
        
        sql = f"""
            INSERT INTO rsucontacts 
            ({columns})
            VALUES ({placeholders})
        """
        
        # Execute SQL insertion
        with engine.connect() as conn:
            conn.execute(text(sql), db_data)
            conn.commit()
        
        return True, "Contact added successfully!"
    except Exception as e:
        return False, f"Database error: {str(e)}"
    
def add_contact_to_rsucontacts(contact_data):
    """
    Insert contact data into the rsucontacts table in the MySQL database.
    
    Args:
        contact_data (dict): Dictionary containing contact details with keys:
            Name, Gender, Designation, Organisation, Department, Group, Email,
            Cell No, Home phone No, Landline / Fax, CNIC, Postal Address,
            Union Council, District, Tehsil
    
    Returns:
        bool: True if insertion is successful, False otherwise
    """
    try:
        if not contact_data.get('Name') or not contact_data.get('Gender'):
            logging.logger.warning("Attempted to insert contact with missing Name or Gender")
            return False
        
        with engine.connect() as conn:
            conn.execute(
                insert(rsucontacts_table),
                contact_data
            )
            conn.commit()
        
        logging.logger.info(f"Contact added successfully: {contact_data['Name']}")
        return True
    
    except Exception as e:
        logging.logger.error(f"Failed to add contact: {str(e)}")
        return False    
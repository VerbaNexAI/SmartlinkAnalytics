from config.db import conn_db

def read_sql_file(file_path):
    """Reads the contents of a SQL file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content

def authenticate_user(email, password):
    """Authenticate user with given email and password.
    
    :param email: User's email.
    :type email: str
    :param password: User's password.
    :type password: str
    :returns: A dictionary with user's first name and last name if authenticated, otherwise None.
    :rtype: dict or None
    """
    sql = read_sql_file(r'C:\Users\santiago.marmol\Desktop\SmarkLink-Api\SmartlinkAnalytics\frontend\config\data\login_valid.sql')

    with conn_db() as conn:
        cur = conn.cursor()
        cur.execute(sql, (email, password))
        rows = cur.fetchall()

        if len(rows) > 0:
            return {"first_name": rows[0][0], "last_name": rows[0][1]}
        return None

def check_email_exists(email):
    """Check if the email already exists in the database.
    
    :param email: User's email.
    :type email: str
    :returns: True if the email exists, False otherwise.
    :rtype: bool
    """
    sql = read_sql_file(r'C:\Users\santiago.marmol\Desktop\SmarkLink-Api\SmartlinkAnalytics\frontend\config\data\verify_user.sql')

    with conn_db() as conn:
        cur = conn.cursor()
        rows = cur.execute(sql, (email,)).fetchall()

        return len(rows) > 0

def register_new_user(first_name, last_name, email, password):
    """Register a new user in the database.
    
    :param first_name: User's first name.
    :type first_name: str
    :param last_name: User's last name.
    :type last_name: str
    :param email: User's email.
    :type email: str
    :param password: User's password.
    :type password: str
    :returns: True if registration is successful, False otherwise.
    :rtype: bool
    """
    try:
        sql = read_sql_file(r'C:\Users\santiago.marmol\Desktop\SmarkLink-Api\SmartlinkAnalytics\frontend\config\data\insert_user.sql')

        with conn_db() as conn:
            cur = conn.cursor()
            cur.execute(sql, (first_name, last_name, email, password))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

import pyodbc
from config import DB_CONFIG

import pyodbc

def get_connection():
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


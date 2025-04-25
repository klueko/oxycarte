import pyodbc

server = 'DESKTOP-91AJVRH\SQLEXPRESS'
database = 'OxycarteDB'

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

cursor = conn.cursor()

create_table_sql = """
IF NOT EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = 'AQI_Stations'
)
BEGIN
    CREATE TABLE AQI_Stations (
        StationID INT IDENTITY(1,1) PRIMARY KEY,
        StationName NVARCHAR(255),
        AQI INT,
        Latitude FLOAT,
        Longitude FLOAT,
        CreatedAt DATETIME DEFAULT GETDATE(),
        PM25 FLOAT,
        PM10 FLOAT,
        NO2 FLOAT,
        CO FLOAT,
        SO2 FLOAT,
        Ozone FLOAT
    );
END
"""

cursor.execute(create_table_sql)
conn.commit()
conn.close()

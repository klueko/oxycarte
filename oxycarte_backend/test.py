import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=OxycarteDB;"
        "Trusted_Connection=yes;"
    )
    print("✅ Connexion réussie à SQL Server !")
except Exception as e:
    print("❌ Erreur de connexion :", e)

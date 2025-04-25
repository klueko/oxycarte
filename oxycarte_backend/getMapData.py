import requests
import pyodbc
import time

token = '8e69591e195d048d9a75b2e555bb34304c64804f'

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=OxycarteDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("Connecté à la base de données")
except pyodbc.Error as e:
    print(f"Erreur de connexion à la base : {e}")
    exit()

latlng_bounds = '42.5,3.5,51.0,7.5'
stations_url = f"http://api.waqi.info/map/bounds/?latlng={latlng_bounds}&token={token}"
response = requests.get(stations_url)
stations_data = response.json()

if stations_data['status'] == 'ok':
    stations = stations_data['data']
    print(f"{len(stations)} stations trouvées.")

    for station in stations:
        uid = station.get('uid')
        detail_url = f"https://api.waqi.info/feed/@{uid}/?token={token}"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()

        if detail_data['status'] == 'ok':
            data = detail_data['data']
            name = data['city']['name']
            aqi = data.get('aqi')
            pm25 = data.get('iaqi', {}).get('pm25', {}).get('v')
            timestamp = data.get('time', {}).get('s')
            forecast = data.get('forecast', {}).get('daily', {}).get('pm25', [])

            for day in forecast:
                try:
                    cursor.execute("""
                        INSERT INTO AQI_Stations (
                            StationName, AQI, PM25, Timestamp,
                            ForecastDate, ForecastMin, ForecastMax, ForecastAvg
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, name, aqi, pm25, timestamp,
                         day['day'], day['min'], day['max'], day['avg'])

                    conn.commit()
                    print(f"Données insérées pour {name} - {day['day']}")
                except pyodbc.Error as e:
                    print(f"Erreur lors de l'insertion SQL : {e}")

        else:
            print(f"⚠️ Station UID {uid} : données non récupérées")

        time.sleep(1)

else:
    print("Impossible de récupérer les stations :", stations_data)

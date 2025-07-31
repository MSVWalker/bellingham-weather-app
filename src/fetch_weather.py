from meteostat import Daily
from datetime import datetime
import duckdb
import pandas as pd

station_id = 'KBLI0'  # Bellingham Airport
start = datetime(1972, 1, 1)
end = datetime.now()

# Fetch and clean
data = Daily(station_id, start, end).fetch().reset_index()
data['time'] = pd.to_datetime(data['time'])
data = data.rename(columns={
    'tavg': 'temp_avg_c',
    'tmin': 'temp_low_c',
    'tmax': 'temp_high_c',
    'prcp': 'precip_mm'
})

# Save to DuckDB
con = duckdb.connect("data/weather.duckdb")
con.execute("CREATE OR REPLACE TABLE weather_data AS SELECT * FROM data")
con.close()

print("✅ Weather data saved to DuckDB.")
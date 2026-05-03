import sqlite3
from datetime import datetime

db_path = "weather.db"

def get_db_connection():
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON") #Active FK
    return con

def init_db():
    con = get_db_connection()
    cur = con.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            longitude REAL NOT NULL,
            latitude REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, country)
        );

        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            temp_min REAL NOT NULL,
            temp_max REAL NOT NULL,
            humidity REAL NOT NULL,
            wind REAL NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
            UNIQUE(city_id, date)
        );      
    """)

    con.commit()
    con.close()
    print("Database initialized")


def insert_city(city: dict) -> int:
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO cities (name, country, longitude, latitude)
        VALUES (:name, :country, :longitude, :latitude)
    """, city)

    con.commit()
    
    cur.execute("""
        SELECT id FROM cities WHERE name = :name AND country = :country
    """, city)

    city_id = cur.fetchone()[0]
    con.close()
    return city_id


def insert_forecast(city_id: int, forecast: list[dict]):
    con = get_db_connection()
    cur = con.cursor()

    actual_date = datetime.now().isoformat()

    cur.executemany("""
        INSERT OR REPLACE INTO forecasts 
            (city_id, date, temp_min, temp_max, humidity, wind, description, icon, collected_at, updated_at)
        VALUES 
            (:city_id, :date, :temp_min, :temp_max, :humidity, :wind, :description, :icon, :collected_at, :updated_at)
    """, [
        {**forecast_item, "city_id": city_id, "collected_at": actual_date, "updated_at": actual_date}
        for forecast_item in forecast
    ])

    con.commit()
    con.close()


def get_forecast_city(city_name: str) -> list[dict]:
    con = get_db_connection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""
        SELECT 
            c.name AS city_name, c.country, c.longitude, c.latitude,
            f.date, f.temp_min, f.temp_max, f.humidity, f.wind, f.description, f.icon
        FROM forecasts f
        JOIN cities c ON f.city_id = c.id
        WHERE LOWER(c.name) = LOWER(:name) AND f.date >= DATE("now")
        ORDER BY f.date ASC LIMIT 14
    """, {"name": city_name})

    rows = cur.fetchall()
    con.close()
    return [dict(row) for row in rows]


def get_history() -> list[dict]:
    con = get_db_connection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""
        SELECT 
            c.name, c.country, c.longitude, MAX(f.updated_at) AS last_updated
        FROM cities c
        JOIN forecasts f ON c.id = f.city_id
        GROUP BY c.id
        ORDER BY last_updated DESC
    """)

    rows = cur.fetchall()
    con.close()
    return [dict(row) for row in rows]



if __name__ == "__main__":
    from api import get_city_info, get_forecast

    init_db()

    city_info = get_city_info("Neuchâtel")
    forecasts = get_forecast(city_info["latitude"], city_info["longitude"])

    city_id = insert_city(city_info)
    print(f"City ID: {city_id}")
    print(f"{city_info['name']}")

    insert_forecast(city_id, forecasts)
    print("forecast inserted")

    r = get_forecast_city("Neuchâtel")
    for item in r:
        print(f"{item['date']} - {item['temp_min']}°C / {item['temp_max']}°C")



CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, country)
);

CREATE TABLE forecasts (
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

CREATE INDEX idx_forecast_city_id ON forecasts(city_id);


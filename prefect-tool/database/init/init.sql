-- init.sql

-- Create the weather_data table
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,  -- Unique identifier for each entry
    date DATE NOT NULL,  -- The date of the weather data
    temperature_c NUMERIC(5, 2),  -- Current temperature in °C
    temperature_k NUMERIC(5, 2),  -- Current temperature in Kelvin
    humidity NUMERIC(5, 2),  -- Current relative humidity in %
    precipitation NUMERIC(5, 2),  -- Current precipitation in mm
    wind_speed NUMERIC(5, 2),  -- Current wind speed in km/h
    max_temperature NUMERIC(5, 2),  -- Maximum temperature for the day in °C
    min_temperature NUMERIC(5, 2)   -- Minimum temperature for the day in °C
);

-- Example of inserting a sample row (you can remove this if not needed)
-- INSERT INTO weather_data (date, temperature, humidity, precipitation, wind_speed, max_temperature, min_temperature)
-- VALUES ('2024-09-02', 25.5, 60.0, 0.0, 15.0, 28.0, 20.0);

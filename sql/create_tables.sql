-- Таблица созвездий
CREATE TABLE constellations (
    constellation_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    latin_name VARCHAR(100) NOT NULL UNIQUE,
    main_stars_count INT DEFAULT 0 CHECK (main_stars_count >= 0),
    area_square_degrees FLOAT NOT NULL CHECK (area_square_degrees > 0)
);

-- Таблица звезд
CREATE TABLE stars (
    star_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    constellation_id INT,
    right_ascension FLOAT NOT NULL CHECK (right_ascension BETWEEN 0 AND 360),
    declination FLOAT NOT NULL CHECK (declination BETWEEN -90 AND 90),
    magnitude FLOAT,
    distance_light_years FLOAT NOT NULL CHECK (distance_light_years > 0),
    FOREIGN KEY (constellation_id) REFERENCES constellations(constellation_id)
);

-- Таблица объектов наблюдения
CREATE TABLE observation_objects (
    object_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    constellation_id INT,
    description TEXT,
    FOREIGN KEY (constellation_id) REFERENCES constellations(constellation_id),
    UNIQUE (name, constellation_id)
);

-- Таблица сезонов наблюдения
CREATE TABLE observation_seasons (
    season_id SERIAL PRIMARY KEY,
    season_name VARCHAR(50) NOT NULL,
    start_month INT NOT NULL CHECK (start_month BETWEEN 1 AND 12),
    end_month INT NOT NULL CHECK (end_month BETWEEN 1 AND 12)
);

-- Промежуточная таблица для связи созвездий и сезонов
CREATE TABLE constellation_seasons (
    constellation_id INT,
    season_id INT,
    PRIMARY KEY (constellation_id, season_id),
    FOREIGN KEY (constellation_id) REFERENCES constellations(constellation_id),
    FOREIGN KEY (season_id) REFERENCES observation_seasons(season_id)
);

-- Таблица исторических фактов
CREATE TABLE historical_facts (
    fact_id SERIAL PRIMARY KEY,
    constellation_id INT,
    fact_text TEXT NOT NULL,
    FOREIGN KEY (constellation_id) REFERENCES constellations(constellation_id)
);

-- Функция для увеличения main_stars_count при добавлении звезды
CREATE OR REPLACE FUNCTION increase_main_stars_count() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE constellations
    SET main_stars_count = main_stars_count + 1
    WHERE constellation_id = NEW.constellation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для увеличения main_stars_count при добавлении звезды
CREATE TRIGGER trg_increase_main_stars_count
AFTER INSERT ON stars
FOR EACH ROW
EXECUTE FUNCTION increase_main_stars_count();

-- Функция для уменьшения main_stars_count при удалении звезды
CREATE OR REPLACE FUNCTION decrease_main_stars_count() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE constellations
    SET main_stars_count = main_stars_count - 1
    WHERE constellation_id = OLD.constellation_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Триггер для уменьшения main_stars_count при удалении звезды
CREATE TRIGGER trg_decrease_main_stars_count
AFTER DELETE ON stars
FOR EACH ROW
EXECUTE FUNCTION decrease_main_stars_count();

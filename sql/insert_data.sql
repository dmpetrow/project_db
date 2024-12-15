INSERT INTO constellations (name, latin_name, area_square_degrees)
VALUES
('Андромеда', 'Andromeda', 722.3),
('Большая Медведица', 'Ursa Major', 1279.7),
('Кассиопея', 'Cassiopeia', 598.4),
('Орион', 'Orion', 594.1),
('Малая Медведица', 'Ursa Minor', 255.9),
('Дева', 'Virgo', 1294.4),
('Геркулес', 'Hercules', 1225.1),
('Дракон', 'Draco', 1082.95),
('Волопас', 'Boötes', 906.8),
('Северная Корона', 'Corona Borealis', 178.7);

INSERT INTO stars (name, constellation_id, right_ascension, declination, 
                   magnitude, distance_light_years) VALUES
('Альферац', 1, 0, 29, 2.06, 97),
('Мирах', 1, 1, 35, 2.05, 199),  
('Аламак', 1, 2, 42, 2.1, 355.8),
('Алиот', 2, 12, 55, 1.77, 81), 
('Дубхе', 2, 11, 61, 1.79, 122.88), 
('Бенетнаш', 2, 13, 49, 1.86, 101),                
('Мицар', 2, 13, 54, 2.23, 78),
('Мерак', 2, 11, 56, 2.37, 25.9),
('Фекда', 2, 11, 53, 2.41, 110.76),
('Шедар', 3, 0, 56, 2.24, 229),
('Каф', 3, 0, 59, 2.28, 47),
('Нави', 3, 0, 60, 2.47, 610),
('Рукбах', 3, 1, 60, 2.66, 99.4),
('Ригель', 4, 5, -8, 0.12, 860),
('Бетельгейзе', 4, 5, 7, 0.6, 548),
('Беллатрикс', 4, 5, 6, 1.64, 243),
('Альнилам', 4, 5, -1, 1.69, 2000),
('Альнитак', 4, 5, -2, 1.72, 817),
('Саиф', 4, 5, -9, 2.06, 647),
('Минтака', 4, 5, 0, 2.23, 900),
('Хатиса', 4, 5, -5, 2.75, 1325.9),
('Полярная звезда', 5, 2, 89, 1.97, 447),
('Кохаб', 5, 14, 74, 2.08, 126),
('Спика', 6, 13, -11, 0.97, 303),
('Поррима', 6, 12, -1, 2.74, 40),
('Виндемиатрикс', 6, 13, 10, 2.79, 108),
('Рас Альгети', 7, 17, 14, 2.74, 329),
('Корнефорос', 7, 16, 21, 2.74, 230),
('Этамин', 8, 17, 51, 2.24, 148),
('Альдибаин', 8, 16, 61, 2.73, 92.1),
('Растабан', 8, 17, 52, 2.79, 380),
('Ицар', 9, 14, 27, 2.7, 203),
('Муфрид', 9, 13, 18, 2.68, 37.2),
('Арктур', 9, 14, 19, -0.05, 36.7),
('Гемма', 10, 15, 26, 2.21, 75);

INSERT INTO observation_objects (name, constellation_id, description)
VALUES
('Андромедиды', 1, 'Метеорный поток'),
('Туманность Андромеды', 1, 'Галактика'),
('Ориониды', 4, 'Метеорный поток'),
('Туманность Ориона', 4, 'Туманность'),
('Трапеция Ориона', 4, 'Звездное скопление'),
('Кассиопея A', 3, 'Остаток сверхновой'),
('Виргиниды', 6, 'Метеорный поток'),
('Январские Боотиды', 9, 'Метеорный поток'),
('Квадрантиды', 9, 'Метеорный поток'),
('Калвера', 5, 'Нейтронная звезда');

INSERT INTO observation_seasons (season_name, start_month, end_month) VALUES
('Зима', 12, 2),
('Весна', 3, 5),
('Лето', 6, 8),
('Осень', 9, 11),
('Зима', 1, 2),
('Весна', 4, 5),
('Лето', 7, 8),
('Лето', 6, 7),
('Осень', 9, 10),
('Осень', 10, 11);

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(1, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 11)),
(1, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 10)),
(1, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 10 AND end_month = 11));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 12 AND end_month = 2)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 3 AND end_month = 5)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 8)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 11)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 1 AND end_month = 2)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 4 AND end_month = 5)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 7)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 7 AND end_month = 8)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 10)),
(2, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 10 AND end_month = 11));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 12 AND end_month = 2)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 3 AND end_month = 5)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 8)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 11)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 1 AND end_month = 2)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 4 AND end_month = 5)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 7)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 7 AND end_month = 8)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 10)),
(3, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 10 AND end_month = 11));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(4, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 12 AND end_month = 2)),
(4, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 1 AND end_month = 2));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 12 AND end_month = 2)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 3 AND end_month = 5)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 8)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 11)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 1 AND end_month = 2)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 4 AND end_month = 5)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 7)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 7 AND end_month = 8)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 10)),
(5, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 10 AND end_month = 11));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(6, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 3 AND end_month = 5)),
(6, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 4 AND end_month = 5));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(7, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 8)),
(7, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 7)),
(7, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 7 AND end_month = 8));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 12 AND end_month = 2)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 3 AND end_month = 5)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 8)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 11)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Зима' AND start_month = 1 AND end_month = 2)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 4 AND end_month = 5)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 7)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 7 AND end_month = 8)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 9 AND end_month = 10)),
(8, (SELECT season_id FROM observation_seasons WHERE season_name = 'Осень' AND start_month = 10 AND end_month = 11));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(9, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 3 AND end_month = 5)),
(9, (SELECT season_id FROM observation_seasons WHERE season_name = 'Весна' AND start_month = 4 AND end_month = 5));

INSERT INTO constellation_seasons (constellation_id, season_id)
VALUES
(10, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 8)),
(10, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 6 AND end_month = 7)),
(10, (SELECT season_id FROM observation_seasons WHERE season_name = 'Лето' AND start_month = 7 AND end_month = 8));

INSERT INTO historical_facts (constellation_id, fact_text)
VALUES
(1, 'Одно из древних созвездий. Включено в каталог звёздного неба Клавдия Птолемея «Альмагест». '),
(2, 'Другой вариант трактовки астеризма отражён в альтернативном названии Катафалк и Плакальщицы.'),
(3, 'Арабы видели в расположении звёзд руку, указывающую пальцем на впереди расположенные звёзды. '),
(4, 'Самым ранним известным изображением, связанным с созвездием Ориона, является доисторическая резьба по кости мамонта, найденная в пещере в долине Ах в Западной Германии в 1979 году. По оценкам археологов, ей от 32 000 до 38 000 лет.'),
(5, 'По утверждению Гайя Юлия Гигина, в античную астрономию это созвездие ввёл Фалес Милетский, включив его в каталог звёздного неба Клавдия Птолемея «Альмагест». '),
(6, 'В большинстве мифов Дева изображается как непорочная дева, ассоциируемая с пшеницей. '),
(7, 'Первоначально созвездие не персонифицировалось и называлось «Коленопреклонённый».'),
(8, 'Шахматный дебют — вариант дракона — также назван в честь созвездия.'),
(9, 'Альтернативное название в Древней Греции — Арктофилакс («Страж медведицы», имеется в виду созвездие Большая Медведица).'),
(10,'Изначально называлась просто Корона или Венец, до выделения созвездия Южная Корона.');
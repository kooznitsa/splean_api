# API для песен группы Сплин

![Static Badge](https://img.shields.io/badge/development-ongoing-yellow)

Технологии:

<img src="https://img.shields.io/badge/Python-800000?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-A52A2A?style=for-the-badge&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/DRF-A52A2A?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-A0522D?style=for-the-badge&logo=PostgreSQL&logoColor=white"/> <img src="https://img.shields.io/badge/Pytest-8B4513?style=for-the-badge&logo=Pytest&logoColor=white"/> <img src="https://img.shields.io/badge/NGINX-BDB76B?style=for-the-badge&logo=NGINX&logoColor=white"/>  <img src="https://img.shields.io/badge/Docker-9a7b4d?style=for-the-badge&logo=Docker&logoColor=white"/> <img src="https://img.shields.io/badge/Elasticsearch-9a7b4d?style=for-the-badge&logo=Elasticsearch&logoColor=white"/>

Swagger: http://127.0.0.1:1337/v1/swagger

Admin: http://127.0.0.1:1337/admin

## Запуск проекта

```bash
git clone https://github.com/kooznitsa/splean_api.git
cd splean_api
cp .env.example .env
// Отредактировать .env
make run
```

## Эндпойнты

- Альбомы:
  - ```albums/```: список всех альбомов
  - ```albums/{id}```: информация об альбоме по ID
  - ```albums/{id}/songs/```: список песен по ID альбома
  - ```albums/stats/```: статистика альбомов: самый старый, самый новый, самый длинный, самый короткий
- Песни:
  - ```songs/```: список всех песен
  - ```songs/{id}```: информация о песне по ID
  - ```songs/{id}/lines```: строки песни по ID песни
  - ```songs/by-year/?year=1999```: все песни данного года
  - ```songs/stats/```: статистика песен: самая длинная, самая короткая, по числу строк, по продолжительности
- Строки:
  - ```lines/```: все строки всех песен
  - ```lines/{id}```: строка по ID
  - ```lines/by-word/?word=мёд```: строки, содержащие определенное слово или фразу
  - ```lines/random/```: случайная строка
  - ```lines/alcohol/```: строки, содержащие упоминания алкогольных напитков
  - ```lines/petersburg/```: строки, содержащие упоминания Петербурга
  - ```lines/winter/```: строки про зиму

## Диаграмма базы данных

![Диаграмма базы данных](https://raw.githubusercontent.com/kooznitsa/splean_api/refs/heads/main/sql_diagram.png)

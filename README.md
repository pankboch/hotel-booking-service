# hotel-booking-service

Simple REST API service for managing hotel rooms and bookings.

## Описание проекта

`hotel-booking-service` — REST API сервис для управления номерами отеля и бронированиями.  
Проект написан на **Django + Django REST Framework** и использует **PostgreSQL** в качестве базы данных.

Сервис позволяет:

- создавать номера;
- получать список всех номеров;
- сортировать номера по `price` и `created_at`;
- удалять номера вместе со связанными бронированиями;
- создавать бронирования для конкретного номера;
- удалять бронирования;
- получать список бронирований конкретного номера;
- проверять пересечение дат при создании бронирований.

Проект также включает API-тесты для основных сценариев работы сервиса: 
- создание номеров и бронирований:
- получение номеров и бронирований;
- удаление номеров и бронирований;
- проверку валидации входных данных;
- пересечения дат;
- граничных случаев бронирования.

## Стек технологий

- Python 3.13
- Django 6
- Django REST Framework
- PostgreSQL
- Poetry
- Ruff
- MyPy
- Bandit
- Radon
- Pre-commit

## Структура проекта

```text
.
├── .env.example
├── Makefile
├── pyproject.toml
├── README.md
└── src
    ├── bookings
    ├── config
    ├── manage.py
    └── rooms
```

## Переменные окружения

Проект использует файл `.env`.  
Шаблон находится в `.env.example`.

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=hotel_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/pankboch/hotel-booking-service
cd hotel-booking-service
```

### 2. Установить зависимости

```bash
pip install poetry
poetry install
```

### 3. Создать `.env`

Создай файл `.env` в корне проекта на основе `.env.example`.

### 4. Создать базу данных PostgreSQL

```sql
CREATE DATABASE hotel_db;
```

### 5. Применить миграции и запустить сервер

```bash
cd src
poetry run python manage.py migrate
poetry run python manage.py runserver
```

После запуска сервис будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

## API endpoints

### Rooms

- `GET /rooms/` — получить список всех номеров
- `POST /rooms/create/` — создать номер
- `DELETE /rooms/delete/<room_id>/` — удалить номер
- `GET /rooms/?ordering=price` — сортировка по цене
- `GET /rooms/?ordering=-price` — сортировка по цене по убыванию
- `GET /rooms/?ordering=created_at` — сортировка по дате создания
- `GET /rooms/?ordering=-created_at` — сортировка по дате создания по убыванию

### Bookings

- `POST /bookings/create/` — создать бронирование
- `DELETE /bookings/delete/<booking_id>/` — удалить бронирование
- `GET /bookings/room/?room_id=1` — получить бронирования конкретного номера

## Примеры запросов

### Создание номера

```bash
curl -X POST http://127.0.0.1:8000/rooms/create/ \
-H "Content-Type: application/json" \
-d '{"description": "Standard room with one double bed", "price": "5500.00"}'
```

Пример ответа:

```json
{
  "new_room_id": 1
}
```

### Получение списка номеров с сортировкой

```bash
curl "http://127.0.0.1:8000/rooms/?ordering=price"
```

### Создание бронирования

```bash
curl -X POST http://127.0.0.1:8000/bookings/create/ \
-H "Content-Type: application/json" \
-d '{"room": 1, "date_start": "2026-03-20", "date_end": "2026-03-23"}'
```

Пример ответа:

```json
{
  "booking_id": 1
}
```

### Получение бронирований номера

```bash
curl "http://127.0.0.1:8000/bookings/room/?room_id=1"
```

Пример ответа:

```json
{
  "room_id": 1,
  "bookings": [
    {
      "id": 1,
      "date_start": "2026-03-20",
      "date_end": "2026-03-23"
    }
  ]
}
```

### Удаление номера

```bash
curl -X DELETE http://127.0.0.1:8000/rooms/delete/1/
```

Пример ответа:

```json
{
  "deleted_room": 1,
  "deleted_bookings": [
    {
      "booking_id": 1,
      "date_start": "2026-03-20",
      "date_end": "2026-03-23"
    }
  ]
}
```

## Проверка качества кода

В проекте есть `Makefile` с готовыми командами:

```bash
make lint
make fmt
make type
make security
make cc
make mi
make check
```

Кратко:

- `make lint` — проверка Ruff с автоисправлением;
- `make fmt` — форматирование кода;
- `make type` — проверка типов через MyPy;
- `make security` — проверка безопасности через Bandit;
- `make cc` — цикломатическая сложность через Radon;
- `make mi` — индекс поддерживаемости через Radon;
- `make check` — запуск всех проверок сразу.

## Планы по доработке

- Docker;
- логирование.

## Автор

**Pankrat**  
Email: `panknotdeadd@gmail.com`

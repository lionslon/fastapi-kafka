# FastAPI Проект для обработки и публикации данных

Система обработки данных для аналитической платформы. Данные поступают в систему через API, сохраняются в PostgreSQL, а затем публикуются в Kafka для последующей обработки другими сервисами.

## Технологии

- `FastAPI`
- `SQLAlchemy (Async)`
- `Kafka (aiokafka)`
- `PostgreSQL`
- `Pydantic`
- `Docker`

## Задание

Создать REST API, которое:
- Принимает JSON данные от пользователя.
- Сохраняет данные в таблице PostgreSQL.
- Валидирует входящие данные.
- Опубликовать эти данные в Kafka.
- Реализовать endpoint для получения списка всех сохраненных записей.

## Требования

### 1. База данных (PostgreSQL)

Создать таблицу data_entries со следующими полями:
* id (serial primary key)
* content (jsonb) — данные в формате JSON
* created_at (timestamp) — время создания записи

### 2. API (FastAPI)

`POST /data`

* Принимает JSON в теле запроса.
* Валидирует наличие поля content (строка, обязательное).
* Сохраняет данные в таблицу data_entries.
* Публикует данные в Kafka с ключом data_entry.
* Возвращает ID сохраненной записи.

`GET /data`

* Возвращает все записи из таблицы data_entries.

### 3. Kafka

Создать продюсер, который публикует каждую запись в тему data_topic.

## Примеры

### Запрос на отправку данных
```http
POST /data

{
    "content": "Hello, Kafka!"
}
```
### Ответ:
```http
{
    "id": 1,
    "message": "Data saved and published to Kafka."
}
```

Ответ запроса получения данных

GET /data

json

Копировать код
```http
[
    {
        "id": 1,
        "content": "Hello, Kafka!",
        "created_at": "2024-12-03T10:00:00"
    }
]
```

## Запуск приложения

### Клонируйте репозиторий:

```console
git clone https://github.com/lionslon/fastapi-kafka.git
```

### Установка .env:

* Создайте файл `.env` в корневой директории и вложите туда переменные (приведен пример):

```python
PG_HOST="localhost"
PG_PORT=5432
PG_USER="postgres"
PG_PASSWORD="postgres"
PG_DB="data_db"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "applications"
```

### Запуск через Docker:

* Запускать проект нужно с помощью следующих команд:

```console
docker-compose up -d
```

### Инициализация топика Kafka:

* Для создания топика Kafka выполните следующую команду:

```console
 docker exec -it fastapi-kafka-kafka-1 echo "/usr/bin/kafka-topics --create --partitions 1 --replication-factor 1 --topic data_topic --bootstrap-server localhost:9092"
 ```

* С помощью данной команды выполнится создание топика Kafka с именем "data_topic" внутри докер контейнера.

### Проверка данных внутри топика Kafka:

* Для проверки данных внутри топика Kafka можно использовать следующую команду:

```console
 /usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic data_topic --from-beginning
 ```
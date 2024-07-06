# Проект "Сервис аренды велосипедов"

Этот проект реализует _backend_ для сервиса аренды велосипедов.

## Функциональные цели

- Регистрация и авторизация пользователей с использованием JWT.
- Получение списка доступных велосипедов.
- Аренда и возврат велосипедов с учетом времени начала и окончания аренды.
- Получение истории аренд пользователем.

## Стек технологий

- **Backend:** Django, Django Rest Framework
- **База данных:** PostgreSQL
- **Тестирование:** PyTest
- **Контейнеризация:** Docker
- **CI/CD:** GitHub Actions

## Развёрнутый проект

Проект развёрнут на облачном сервере. Документация API доступна по адресу:
* Интерфейс: http://89.223.123.154/api/v1/schema/swagger-ui/
* Файл в формате _yaml_: http://89.223.123.154/api/v1/schema/

## Установка и запуск
### Подготовка
1. Склонируйте репозиторий:
    ```shell
    git clone https://github.com/TomatoInOil/bike-rental-backend.git
    ```

2. Скопируйте файл `.env.example` под именем `.env`
   ```shell
   cp .env.example .env
   ```

3. Откройте файл `.env` и заполните переменные окружения согласно примеру

> [!NOTE]
> Если планируете разворачивать проект локально через _Docker_, задайте путь к настройкам следующим образом:
> ```text
> DJANGO_SETTINGS_MODULE=app.settings.docker
> ```

### Локально (режим разработчика)
**Требования:**
* Poetry ([документация](https://python-poetry.org/docs/#installation))

**Шаги:**

1. Установите зависимости:
   ```shell
   poetry install
   ```

2. Перейдите в директорию `src/backend`
   ```shell
   cd src/backend/
   ```

3. Примените миграции:
    ```shell
    python manage.py migrate
    ```

    2.1. Наполните БД данными: _(Опционально)_
    ```shell
    python manage.py loaddata fixtures/fake_data.json
    ```

    2.2 Создайте суперпользователя для доступа к админке: _(Опционально)_
    ```shell
    python manage.py createsuperuser
    ```

4. Запустите сервер разработки:
    ```shell
    python manage.py runserver
    ```

Админка будет доступна по адресу: http://127.0.0.1:8000/admin/

Документация API будет доступна по адресу:
* Интерфейс: http://127.0.0.1:8000/api/v1/schema/swagger-ui/
* Файл в формате _yaml_: http://127.0.0.1:8000/api/v1/schema/

### Через Docker

**Требования:**
* Docker ([документация](https://docs.docker.com/desktop/))

**Шаги:**

1. Запустите контейнеры:
   ```shell
   docker compose --file infra/docker-compose.yml up -d
   ```

2. Наполните БД данными: _(Опционально)_
   ```shell
   docker exec backend python backend/manage.py loaddata \
       backend/fixtures/fake_data.json
   ```

3. Создайте суперпользователя для доступа к админке: _(Опционально)_
   ```shell
   docker exec -it backend python backend/manage.py createsuperuser
   ```

Админка будет доступна по адресу: http://127.0.0.1/admin/

Документация API будет доступна по адресу:
* Интерфейс: http://127.0.0.1/api/v1/schema/swagger-ui/
* Файл в формате _yaml_: http://127.0.0.1/api/v1/schema/

## Запуск тестов
Находясь в корневой директории проекта выполните команду:
```shell
pytest
```
Аргументы командной строки заданы в конфигурационном файле `pytest.ini`.

## Примеры запросов
### Регистрация нового пользователя
**Запрос:**
```http request
POST /api/v1/users/registration/
Content-Type: application/json

{
  "username": "example_user",
  "email": "user@example.com",
  "password": "strongpassword"
}
```
**Ответ (успешно):**
```json
{
  "username": "example_user",
  "email": "user@example.com"
}
```

### Получение _access_ токена
**Запрос:**
```http request
POST /api/v1/token/
Content-Type: application/json

{
  "username": "example_user",
  "password": "strongpassword"
}
```
**Ответ (успешно):**
```json
{
  "refresh": "string",
  "access": "string"
}
```


### Получение списка доступных велосипедов
**Запрос:**
```http request
GET /api/v1/bikes/
Authorization: Bearer your_access_token
```
**Ответ (успешно):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "serial_number": "BVX123",
      "rental_cost_per_hour": 150
    },
    {
      "id": 21,
      "serial_number": "OKM789",
      "rental_cost_per_hour": 110
    }
  ]
}
```

### Аренда велосипеда
**Запрос:**
```http request
POST /api/v1/rentals/start/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "bike": 21
}
```
**Ответ (успешно):**
```json
{
  "user": 3,
  "bike": 21,
  "start_time": "2024-07-06T17:05:08.373554+03:00",
  "end_time": null,
  "total_cost": null,
  "status": "Действующая аренда"
}
```

### Завершение аренды
**Запрос:**
```http request
PATCH /api/v1/rentals/end/
Authorization: Bearer your_access_token
Content-Type: application/json

{}
```
**Ответ (успешно):**
```json
{
  "user": 3,
  "bike": 21,
  "start_time": "2024-07-06T17:05:08.373554+03:00",
  "end_time": "2024-07-06T18:06:04.836310+03:00",
  "total_cost": 111.73,
  "status": "Завершенная аренда"
}
```

### Получение истории аренд пользователя
**Запрос:**
```http request
GET /api/v1/rentals/
Authorization: Bearer your_access_token
```
**Ответ (успешно):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "user": 3,
      "bike": 1,
      "start_time": "2024-07-06T18:08:19.158815+03:00",
      "end_time": "2024-07-06T19:08:48.875333+03:00",
      "total_cost": 151.24,
      "status": "Завершенная аренда"
    },
    {
      "user": 3,
      "bike": 21,
      "start_time": "2024-07-06T17:05:08.373554+03:00",
      "end_time": "2024-07-06T18:06:04.836310+03:00",
      "total_cost": 111.73,
      "status": "Завершенная аренда"
    }
  ]
}
```

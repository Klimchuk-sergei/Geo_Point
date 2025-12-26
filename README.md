# GeoPoint API

## Backend на Django для работы с географичесими точками.
## Пользователь может создавать метки на карте, дополнять их сообщениями и искать точки в заданном радиусе.

### Технический стек

- Python 3.11
- Django 5 +DRF
- BD PostgreSQL + PostGIS
- JWT авторизация
- Django APITestCase тестирование
- Docker + Docker compose запуск приложения

### Запуск проекта
1. Клонируйте репозиторий
```commandline
git clone https://github.com/Klimchuk-sergei/Geo_Point.git
```
2. Настройте ваш файл .env, изменив .env.axample внеся необходимые изменения.
3. запустите проект через Docker
docker-compose up --build
4. выполните миграции
docker-compose exec web python manage.py migrate
5. для создания админа используйте
6. docker-compose exec web python manage.ry createsuperuser

# API эндпоинты
### базовый URL доступа 
```
http://127.0.0.1:8000/api/
```

- ### авторизация
для получения доступа необходимо получить токен авторизации.
```
POST /token/
- BODY: {"username": "user", "password": "password""}
- RESPONSE:{"access": "***", "refresh", "***"}

```
### используйте access токен во всех запросах

# Работа с точками
1. Создание точки
```
- url: POST /points/
- body
```
```json
{
    "name": "Кофейня на углу",
    "description": "Отличный латте",
    "location": {
        "type": "Point",
        "coordinates": [37.6173, 55.7558]
    }
}
```
2. ПОиск точек
```text
URL: GET /points/search/
```
```text
Параметры:
    - latitude(float): координата широты точки
    - longitude(float): кордината долготы точки
    - radius(float): радиус поиска в метрах
```
3. Действия с точками
```text
    - GET /points/ — Список всех точек
    - GET /points/{id}/ — Детали точки
    - DELETE /points/{id}/ — Удалить точку (доступно только создателю)
```

## Сообщения на точках
1. Добавить сообщение к точке
```text
    - URL: POST /points/messages/
```
```json
{
    "point": 1,
    "message": "Нашел клад!!!"
}
```
2. Поиск сообщений
находит сообщения точек в указанном радиусе
```text
    - URL: GET /points/messages/search/

    - Параметры: latitude, longitude, radius
```

# Тестирование
Запуск тестов производить внутри запущенного контейнера
```dockerfile
docker-compose exec web python manage.py test
```
Тестируется:
1. Авторизация и доступ не авторизованных юзеров
2. Создание точек на карте
3. Корректность поиска в радиусе и фильтрация по дистанции
4. Запрет на удаление чужих точек (права доступа)

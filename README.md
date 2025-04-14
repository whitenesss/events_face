# Events Face Service

Микросервис для управления мероприятиями с аутентификацией JWT и синхронизацией данных.

## 🛠 Технологии
- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker
- Gunicorn
- JWT аутентификация

## 🚀 Запуск проекта

### Требования
- Docker
- Docker Compose

### Клонирование репозитория
```bash
https://github.com/whitenesss/events_face.git
cd events-face
```
### Создайте .env файл:
```bash
cp .env.example .env
```

### Запуск в Docker
```bash
docker-compose up --build
```
Сервис будет доступен по адресу:
http://localhost:8000/

### 📚 API Endpoints
Аутентификация
POST /api/auth/register - Регистрация

POST /api/auth/login - Вход

POST /api/auth/logout - Выход

POST /api/auth/token/refresh - Обновление токена

Мероприятия
GET /api/events/ - Список мероприятий

GET /api/events/?name=конференция - Фильтрация по названию

GET /api/events/?ordering=-date - Сортировка по дате


### Админка
http://localhost:8000/admin/
(требуется создать суперпользователя)

### 🔧 Управление
Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

### Синхронизация мероприятий
```bash
docker-compose exec web python manage.py sync_events
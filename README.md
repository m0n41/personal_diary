# 🎬 Каталог фильмов с рейтингами

Веб-приложение на Django для просмотра каталога фильмов, оценки фильмов пользователями и поиска с сортировкой.

## ✨ Возможности

- **Просмотр списка фильмов** с возможностью поиска по названию
- **Сортировка** по году выпуска или длительности
- **Детальная страница фильма** с информацией и средним рейтингом
- **Добавление оценок** пользователями (от 1 до 5 ★)
- **Рекомендуемые фильмы** (отдельный менеджер)
- **Автоматическая генерация slug** из названия
- **Визуальное отображение рейтинга** звёздами (кастомный тег)

## 🛠 Технологии

- Python 3.11+
- Django 5.2
- SQLite (по умолчанию)
- HTML/CSS

## 📦 Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/magamamed849/movie-catalog.git
cd movie-catalog
```

### 2. Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Установить зависимости
```bash
pip install django django-extensions unidecode
```

### 4. Выполнить миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Заполнить базу данных тестовыми данными
```bash
python manage.py shell
# Выполнить команду из файла populate_data.py
```

### 6. Запустить сервер
```bash
python manage.py runserver
```

### 7. Открыть в браузере
```text
http://127.0.0.1:8000/core/
```

## 📁 Структура проекта
```text
mysite/
├── core/                    # Основное приложение
│   ├── models.py           # Модели Movie, Rating
│   ├── views.py            # Представления movie_list, movie_detail
│   ├── urls.py             # Маршруты
│   ├── templatetags/       # Кастомные теги (звёзды)
│   ├── templates/core/     # Шаблоны
│   └── context_processors.py # Контекст-процессор для текущего года
├── mysite/                 # Настройки проекта
└── db.sqlite3              # База данных
```

## 🧪 Примеры запросов

| Цель | URL |
| :--- | :--- |
| Список фильмов | `/core/` |
| Поиск по названию | `/core/?q=Нолан` |
| Сортировка по году | `/core/?sort=year` |
| Сортировка по длительности | `/core/?sort=duration` |
| Детальная страница | `/core/gladiator/` |

## 🎯 Модели данных

### Movie
| Поле | Тип | Описание |
| :--- | :--- | :--- |
| name | CharField | Название фильма |
| slug | SlugField | Уникальный идентификатор (авто) |
| director | CharField | Режиссёр |
| release_year | IntegerField | Год выпуска |
| duration | IntegerField | Длительность (мин) |
| description | TextField | Описание |
| is_recommended | BooleanField | Рекомендуемый |
| date_added | DateTimeField | Дата добавления |

### Rating
| Поле | Тип | Описание |
| :--- | :--- | :--- |
| movie | ForeignKey | Связь с фильмом |
| username | CharField | Имя пользователя |
| rating | IntegerField | Оценка (1–5) |
| created_at | DateTimeField | Дата создания |

## 👨‍💻 Менеджеры

- `Movie.objects.all()` — все фильмы
- `Movie.recommended.all()` — только рекомендуемые

## 🎨 Кастомный тег

Отображение рейтинга звёздами:

```django
{% load catalog_tags %}
{% test_inclusion_tag 4.5 %}
```

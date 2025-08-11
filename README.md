
# Сравнение баз данных PostgreSQL

Приложение на Flask для сравнения двух баз данных PostgreSQL по структуре таблиц и содержимому.

---

## Структура проекта

```

.
├── app.py
├── config.json              # Конфигурация (необязательный, если используете форму)
├── config.sample.json       # Пример конфигурации
├── Dockerfile
├── requirements.txt
├── **pycache**
│   └── config.cpython-310.pyc
└── templates
├── db\_form.html         # Форма ввода параметров подключения
└── diff\_report.html     # Отчёт о различиях в базе (HTML шаблон)

```

---

## Установка и запуск локально

1. Клонируйте репозиторий:

   ```bash
   git clone <URL_репозитория>
   cd <папка_репозитория>
   ```

2. Установите зависимости:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   pip install -r requirements.txt
   ```

3. Запустите приложение:

   ```bash
   python app.py
   ```

4. Откройте в браузере: [http://localhost:5000](http://localhost:5000)

---

## Использование

* На стартовой странице заполните параметры подключения к двум PostgreSQL базам (или загрузите JSON файл с настройками).
* Нажмите **"Сравнить"**.
* Вы получите HTML отчёт с различиями по таблицам, структуре и данным.

---

## Формат JSON файла конфигурации

```json
{
  "DB1": {
    "dbname": "имя_базы_1",
    "user": "пользователь_1",
    "password": "пароль_1",
    "host": "хост_1",
    "port": 5432
  },
  "DB2": {
    "dbname": "имя_базы_2",
    "user": "пользователь_2",
    "password": "пароль_2",
    "host": "хост_2",
    "port": 5432
  }
}
```

---

## Запуск в Docker

1. Соберите образ:

   ```bash
   docker build -t pg-db-compare .
   ```

2. Запустите контейнер:

   ```bash
   docker run -p 5000:5000 pg-db-compare
   ```

3. Откройте [http://localhost:5000](http://localhost:5000)

---

## Зависимости

* Python 3.10+
* Flask
* psycopg2-binary
* Bootstrap (через CDN в шаблонах)

---

## Лицензия

MIT License

---

## Контакты

Если есть вопросы или предложения, открывайте issue или пишите.

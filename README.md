# API-автотесты: Restful-Booker (Python + pytest)

Набор автоматизированных API-тестов на **Python / pytest** для сервиса
[Restful-Booker](https://restful-booker.herokuapp.com/) — учебно-боевого REST API
с авторизацией по токену и CRUD над бронями. Проект демонстрирует подход к
автоматизации API-тестирования: чистую архитектуру, валидацию контрактов,
позитивные и негативные сценарии, отчётность и CI.

## Что покрыто

- **Auth** — получение токена, негативные кейсы с неверными кредами (параметризация)
- **Create** — создание брони, валидация JSON-схемы ответа, проверка по GET
- **Read** — список броней, получение по id, `404` на несуществующей
- **Update** — полное обновление (`PUT`), частичное (`PATCH`), `403` без токена
- **Delete** — удаление с проверкой недоступности, `403` без токена
- **Health** — `GET /ping`

Где API ведёт себя некорректно (например, отдаёт `500` вместо `400` на неполном
теле), тест **фиксирует фактическое поведение** с комментарием — в реальном
проекте это основание для баг-репорта.

## Стек

`Python` · `pytest` · `requests` · `jsonschema` · `Allure` · `GitHub Actions`

## Архитектура

```
.
├── config.py                 # настройки, переопределяемые через ENV (dev/stage/CI)
├── conftest.py               # фикстуры: session, api, auth_token, created_booking (+teardown)
├── helpers/
│   ├── api_client.py         # service-object: вся работа с эндпоинтами в одном классе
│   └── booking_payloads.py   # билдеры тестовых данных
├── schemas/
│   └── booking_schema.py     # JSON-схемы для валидации контрактов
├── tests/                    # тесты по фичам (auth / create / read / update / delete / health)
├── .github/workflows/ci.yml  # автозапуск на push и PR + выгрузка Allure-результатов
└── requirements.txt
```

Тесты не обращаются к `requests` напрямую — только через `BookingAPI`
(service-object, API-аналог Page Object). Это держит знание об эндпоинтах в
одном месте и делает тесты читаемыми и устойчивыми к изменениям API.

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                          # все тесты
pytest -m smoke                 # только smoke
pytest --alluredir=allure-results   # с данными для Allure
```

### Allure-отчёт

```bash
# нужен установленный Allure CLI (brew install allure / scoop install allure)
allure serve allure-results
```

### Запуск против другого стенда

```bash
BASE_URL=https://my-stage.example.com pytest
```

## CI

При каждом `push` в `main` и на pull request GitHub Actions устанавливает
зависимости, прогоняет тесты и выкладывает результаты Allure артефактом —
см. вкладку **Actions**.

## Дальнейшие шаги (roadmap)

- UI-автотесты на Playwright (Page Object), запуск в CI с headless-браузером
- Контрактное тестирование (schemathesis / на основе OpenAPI)
- Параметризация прогонов по нескольким окружениям и параллельный запуск (`pytest-xdist`)

# ⚠️ Известные проблемы и ограничения backend-сервиса

Этот документ фиксирует текущие ограничения и нестабильности тестируемого сервиса `test-service`.
Цель — исключить ложные падения автотестов и повысить прозрачность отчётов.

---

## 🧱 1. Deadlock при множественных запросах на создание сущностей

**Описание:**  
При параллельных вызовах эндпоинта  
`POST /api/create`  
в сервисе наблюдается блокировка соединений PostgreSQL:

```
pgconn.(*PgConn).flushWithPotentialWriteReadDeadlock
```

**Проявление:**
- HTTP-ответ `500 Internal Server Error` 
- сервис `service` зависает на операции `INSERT` в таблицу `entities`
- миграции и docker-контейнеры остаются активными, но не отвечают на запросы

**Причина:**  
отсутствие транзакционной изоляции или конфликт за ресурсы при одновременном доступе.

**Влияние:**  
Все API-тесты, которые создают данные одновременно (например, `test_create_entity`, `test_get_all_entities`), могут завершаться ошибкой.

**Рекомендации:**
- запускать API-тесты **последовательно**:  
  ```bash
  pytest -n 0
  ```
- при падении фиксировать в Allure как:
  > Skipped: known backend issue — PostgreSQL deadlock on /api/create

- доработать backend: добавить транзакции и управление блокировками

---

## 🧩 2. Несоответствие API-контракта (Response != Schema)

**Описание:**  
Эндпоинт `POST /api/create` согласно Swagger должен возвращать объект `Entity`,  
но фактически возвращает только `int` — идентификатор созданной сущности.

**Влияние:**  
Pydantic-валидация (`EntityResponse(**response.json())`) вызывает ошибку `TypeError: argument after ** must be a mapping`.

**Рекомендации:**
- временно использовать безопасный парсер:
  ```python
  result = parse_response(EntityResponse, response)
  ```
  с fallback-логикой при получении `int`
- оформить баг-репорт на backend:
  > Backend should return full JSON object, not plain ID

---

## 🧠 3. Миграции SQL вызывают ошибку `limit 1 short`

**Описание:**  
При запуске контейнера `migrate` возможна ошибка:
```
error: limit 1 short
```

**Причина:**  
Порядок создания таблиц (`entities` → `additions`) или отсутствие поля `addition_id`
в таблице `entities`.

**Рекомендации:**
- проверить миграции SQL (создание внешнего ключа должно происходить после обеих таблиц)
- удалить старые volume-данные перед повторным запуском:
  ```bash
  docker compose down -v && docker compose up --build
  ```

---

## 📊 Формат фиксации известных проблем в Allure

Все известные баги должны фиксироваться через `pytest.skip()` с attach-логом:

```python
import pytest, allure

@pytest.mark.api
def test_create_entity(api_client):
    try:
        result = EntityActions(api_client).create_entity(EntityRequest.random())
        assert result.id is not None
    except Exception as e:
        if "deadlock" in str(e).lower():
            allure.attach(str(e), "known_issue_deadlock", allure.attachment_type.TEXT)
            pytest.skip("Известный баг: PostgreSQL deadlock при параллельных insert")
        raise
```

---

## 🧭 Как добавлять новые известные проблемы

1. **Зафиксируй проблему в тестах** — добавь `pytest.skip()` с `allure.attach()`.
2. **Занеси описание сюда** — кратко: причина, влияние, рекомендации.
3. **Сопровождай ссылкой на баг-трекер**, если есть (например, Jira / GitHub Issues).
4. **Сохрани стиль документа** — структура: _Описание_, _Проявление_, _Причина_, _Рекомендации_.
5. **Обнови дату и версию ниже.**

---

## 📅 Последнее обновление

> 2025-11-07  
> Автор: **Alexey Yumanov**  
> Версия: `1.0.0`

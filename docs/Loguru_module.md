## Документация по Loguru (очень подробное объяснение)

Цель этого текста — не просто перечислить возможности Loguru,
а объяснить ключевые идеи **простым языком**, так чтобы
разобрался человек, который впервые настраивает логирование в Python.

---

### 1. Что такое Loguru и зачем он нужен

Когда мы запускаем программу или сервис, нам важно понимать:

- что именно происходит;
- где и почему возникла ошибка;
- как связаны события (по контексту: запрос/пользователь/подсистема).

В Python есть стандартный модуль `logging`, но он часто требует заметной настройки: логгер, handler, formatter, уровни, и т.д.

**Loguru** упрощает старт и даёт много возможностей “из коробки”:

- готовый `logger` без ручной инициализации;
- удобное добавление sink’ов (консоль/файл/JSON) через `logger.add(...)`;
- удобную работу с исключениями (`logger.exception()`, `@logger.catch`);
- контекстные поля `extra` через `bind()` и `contextualize()`;
- ротацию/хранение/сжатие файлов и сериализацию в JSON.

Установка:

```bash
pip install loguru
```

---

### 2. Главный объект: `logger`

Минимальный пример:

```python
from loguru import logger

logger.info("Привет! Это INFO‑сообщение.")
```

Логгер хранит и выводит не только сообщение, но и поля записи: время, уровень, место в коде, и контекст `extra`.

---

### 3. Уровни логирования (DEBUG/INFO/…)

Уровень — это “важность” сообщения. Типовая шкала:

- `DEBUG` — детали, полезно при разработке;
- `INFO` — нормальный рабочий поток;
- `WARNING` — подозрительно, но продолжаем;
- `ERROR` — ошибка: операция не выполнена;
- `CRITICAL` — серьёзная проблема.

Пример:

```python
logger.debug("DEBUG — детали для отладки")
logger.info("INFO — обычное сообщение")
logger.warning("WARNING — предупреждение")
logger.error("ERROR — ошибка")
logger.critical("CRITICAL — критическая ошибка")
```

Какие уровни реально попадут в вывод — зависит от настроек sink’ов (`level=...`).

---

### 4. Sink’и: куда пишутся логи

Sink — это “приёмник” логов. В Loguru sink’ов может быть несколько одновременно:

- консоль (для человека);
- файл `.log` (для истории);
- JSON Lines `.jsonl` (для машинного анализа);
- отдельный файл по фильтру (например, только события БД).

Идея: одна запись логов “проходит” и попадает во все sink’и, которые её принимают.

---

### 5. Базовая конфигурация: `remove()` и `add()`

Частая практика:

```python
logger.remove()
logger.add(sink, level="INFO", format="{time} | {level} | {message}")
```

`remove()` помогает избежать дублирования и держать конфигурацию в одном месте.

---

### 6. Форматирование: `format=...` и плейсхолдеры

Пример формата:

```python
logger.add(
    sink,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {message} | {extra}",
)
```

Важные плейсхолдеры:

- `{time:...}` — время;
- `{level}` — уровень;
- `{message}` — сообщение;
- `{extra}` — контекстные поля.

И форматирование сообщения:

```python
logger.info("User id = {}", 42)
```

---

### 7. Кастомные уровни: `logger.level()` и `logger.log()`

Можно объявить уровень, например NOTICE:

```python
logger.level("NOTICE", no=25, color="<yellow>", icon="!")
logger.log("NOTICE", "Это NOTICE (между INFO и WARNING)")
```

---

### 8. Производительность: `logger.opt(lazy=True)`

Если вычисление дорогое, полезно сделать его “ленивым”:

```python
logger.opt(lazy=True).debug("Результат: {}", expensive)
```

Callable вычислится только если запись реально будет залогирована (а не отфильтрована уровнем).

---

### 9. Контекст: `bind()` и `contextualize()`

`bind()` добавляет `extra`‑поля к логгеру:

```python
log = logger.bind(user_id=42, topic="db")
log.info("Эта запись содержит extra")
```

`contextualize()` добавляет поля внутри блока:

```python
with logger.contextualize(request_id="req_123"):
    logger.info("request_id будет в extra")
```

---

### 10. Фильтрация: `filter=...`

Sink может принимать только часть записей:

```python
def only_db(record):
    return record["extra"].get("topic") == "db"

logger.add("logs/db_only.log", filter=only_db)
```

---

### 11. Исключения: `logger.exception()` и `@logger.catch`

В `except` удобно:

```python
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Произошла ошибка")
```

`@logger.catch` логирует исключения внутри функции:

```python
@logger.catch(reraise=False)
def will_fail():
    {}["missing_key"]
```

---

### 12. `patch()`: автоматическое добавление полей

```python
def add_app(record):
    record["extra"]["app"] = "loguru-guide"

patched = logger.patch(add_app)
patched.info("extra.app добавится автоматически")
```

---

### 13. `disable()` / `enable()`: отключение логов для модуля

```python
module_name = __name__
logger.disable(module_name)
logger.info("Это не выведется")
logger.enable(module_name)
logger.info("А это снова выведется")
```

---

### 14. Файлы: rotation / retention / compression / serialize

Пример:

```python
logger.add(
    "logs/app_{time:YYYYMMDD_HHmmss}.log",
    rotation="25 KB",
    retention=5,
    compression="zip",
    encoding="utf-8",
)
```

JSON Lines:

```python
logger.add("logs/app_{time:YYYYMMDD}.jsonl", serialize=True)
```

---

### 15. Связь с этим проектом

В `guide_loguru.py` демонстрируются все ключевые идеи:

- консольный формат и уровни;
- файловые sink’и (текст + JSON + фильтр);
- контекст `extra`;
- исключения (`exception/catch`);
- `lazy`, `patch`, `disable/enable`.


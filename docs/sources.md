# Использованные источники

- **Официальная документация Loguru**
 Основной источник по API: `logger.add/remove`, форматы, уровни, `bind/contextualize`, `filter`, `patch`, `opt(lazy=True)`, обработка исключений, rotation/retention/compression, `serialize`.

 Ссылка: https://loguru.readthedocs.io/

- **Репозиторий Loguru на GitHub**
 Полезен для чтения примеров, обсуждений и уточнения поведения в edge‑cases.

 Ссылка: https://github.com/Delgan/loguru

- **Документация Python по стандартному логированию (для сравнения подходов)**
 Использовалась, чтобы понимать, какие проблемы решают альтернативные библиотеки и как устроены уровни/форматы в базовом `logging`.

 Ссылка: https://docs.python.org/3/library/logging.html

- **Собственные эксперименты с запуском `guide_loguru.py`**
 На практике проверялись: вывод в консоль, создание `logs/`, ротация, JSON‑лог, фильтрация по `extra`, поведение `logger.exception()` и `@logger.catch`.


- **Документация Python `logging`**
 (для сравнения): https://docs.python.org/3/library/logging.html
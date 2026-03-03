# loguru-guide — публичный API (учебный)

Этот проект не является библиотекой с импортируемым пакетом — это демонстрационный скрипт `guide_loguru.py`.
Тем не менее у него есть “публичные” функции, которые формируют архитектуру демо.

## Точка входа

- `run()` — настраивает Loguru и последовательно запускает демонстрации.

## Конфигурация логирования

- `configure_console()` — настраивает консольный sink:
  - убирает дефолтные sink’и через `logger.remove()`
  - добавляет sink‑функцию `sink_print(...)`
  - задаёт формат, уровень и опции диагностики

- `configure_files()` — настраивает файловые sink’и в `logs/`:
  - текстовый лог с `rotation/retention/compression`
  - JSON Lines (`serialize=True`)
  - отдельный файл с фильтром по `extra` (например, `topic="db"`)

## Визуальная структура вывода

- `section(title)` — печатает заголовок раздела (рамка + название), чтобы вывод был читаемым.
- `sink_print(message)` — sink‑функция, печатает сформированное Loguru сообщение в консоль.

## Демонстрации возможностей Loguru

- `demo_basics()` — базовые уровни (`DEBUG/INFO/WARNING/ERROR/CRITICAL`)
- `demo_custom_level()` — кастомный уровень через `logger.level(...)` и `logger.log(...)`
- `demo_formatting_and_lazy()` — форматирование и `logger.opt(lazy=True)` (ленивые вычисления)
- `demo_bind_and_context()` — контекст: `bind()` и `contextualize()`
- `demo_filtering()` — фильтрация (sink с `filter=...`) по `extra`‑полям
- `demo_exceptions()` — `logger.exception()` и `@logger.catch`
- `demo_patch()` — `patch()` для автоматического добавления/изменения полей записи
- `demo_disable_enable()` — `disable()/enable()` для отключения логов по имени модуля

## Артефакты после запуска

После выполнения `run()` проект ожидаемо оставляет в `logs/`:

- текстовые логи с ротацией и архивами
- JSON Lines (`.jsonl`)
- фильтрованный лог (например, `db_only.log`)


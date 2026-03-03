from loguru import logger


def sink_print(message) -> None:
    # `message` уже содержит перенос строки; end="" не дублирует его.
    print(message, end="")


def section(title: str) -> None:
    logger.info("")
    logger.info("=" * 88)
    logger.info("{}", title)
    logger.info("=" * 88)


def configure_console() -> None:
    """
    Базовая настройка консольного вывода.
    Важно: по условию задачи этот файл импортирует только `loguru`.
    """
    logger.remove()
    logger.add(
        sink_print,
        level="DEBUG",
        colorize=True,
        backtrace=True,
        diagnose=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "{message} "
            "<blue>{extra}</blue>"
        ),
    )


def configure_files() -> None:
    """
    Несколько файловых sink'ов: обычный текст, JSON, и пример фильтрации.
    Loguru сам создаёт директории (например, `logs/`) при необходимости.
    """
    logger.add(
        "logs/app_{time:YYYYMMDD_HHmmss}.log",
        level="DEBUG",
        rotation="25 KB",
        retention=5,
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message} | {extra}",
    )

    # Машиночитаемые логи: JSON Lines (по строке JSON на запись).
    logger.add(
        "logs/app_{time:YYYYMMDD}.jsonl",
        level="INFO",
        rotation="50 KB",
        serialize=True,
        encoding="utf-8",
    )

    # Фильтрация: писать в файл только записи с extra={"topic": "db"}.
    def only_db(record) -> bool:
        return record["extra"].get("topic") == "db"

    logger.add(
        "logs/db_only.log",
        level="DEBUG",
        filter=only_db,
        rotation="25 KB",
        retention=3,
        encoding="utf-8",
        format="{time:HH:mm:ss} | {level} | {message} | {extra}",
    )


def demo_basics() -> None:
    section("1) Базовые уровни и сообщения")
    logger.debug("DEBUG — обычно много деталей, полезно при разработке.")
    logger.info("INFO — нормальный рабочий поток приложения.")
    logger.warning("WARNING — что-то подозрительное, но продолжаем.")
    logger.error("ERROR — ошибка: операция не выполнена.")
    logger.critical("CRITICAL — серьёзная проблема.")


def demo_custom_level() -> None:
    section("2) Кастомный уровень (level)")
    logger.level("NOTICE", no=25, color="<yellow>", icon="!")
    logger.log("NOTICE", "Это уровень NOTICE (между INFO и WARNING).")


def demo_formatting_and_lazy() -> None:
    section("3) Форматирование и lazy‑вычисления (opt(lazy=True))")

    calls = {"n": 0}

    def expensive() -> str:
        calls["n"] += 1
        return f"expensive_result_{calls['n']}"

    # TRACE ниже DEBUG, а наши sink'и настроены с level="DEBUG".
    # Значит TRACE-сообщения НЕ будут записаны, и это можно использовать для наглядной демонстрации:
    # - без lazy вычисление происходит ДО вызова логгера (и случится даже если запись отфильтруется)
    # - с lazy callable вычислится только если запись реально будет залогирована
    logger.trace("Без lazy (expensive() вычислится заранее): {}", expensive())
    logger.opt(lazy=True).trace("С lazy (callable НЕ будет вычислен): {}", expensive)
    logger.info("Итог: expensive вызвали {} раз(а) (ожидаем 1).", calls["n"])

    # На уровне INFO сообщение проходит, поэтому callable будет вычислен.
    logger.opt(lazy=True).info("А тут callable вычислится: {}", expensive)
    logger.info("Теперь expensive вызвали {} раз(а).", calls["n"])


def demo_bind_and_context() -> None:
    section("4) Контекст: bind() и contextualize()")

    log = logger.bind(app="guide", user_id=42)
    log.info("bind() добавляет поля в extra для конкретного логгера.")

    logger.info("Без bind/contextualize extra обычно пустой: {}", "ok")

    with logger.contextualize(request_id="req_123", path="/health"):
        logger.info("contextualize() добавляет extra внутри блока.")
        with logger.contextualize(user_id=7):
            logger.info("Вложенный contextualize() переопределяет/добавляет extra.")


def demo_filtering() -> None:
    section("5) Фильтрация (filter=...) по extra-полям")

    logger.bind(topic="db").debug("Эта запись попадёт в logs/db_only.log (topic=db).")
    logger.bind(topic="http").debug("А эта — не попадёт (topic=http).")
    logger.debug("И эта — тоже не попадёт (topic отсутствует).")


def demo_exceptions() -> None:
    section("6) Исключения: logger.exception() и @logger.catch")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("logger.exception() автоматически подхватывает текущий exception.")

    @logger.catch(reraise=False)
    def will_fail() -> None:
        # Любая ошибка будет залогирована. reraise=False: не пробрасываем дальше.
        d = {}
        _ = d["missing_key"]

    will_fail()
    logger.info("После @logger.catch выполнение продолжается.")


def demo_patch() -> None:
    section("7) patch(): автоматически добавлять/менять поля записи")

    def add_app_field(record) -> None:
        record["extra"]["app"] = "loguru-guide"

    patched = logger.patch(add_app_field)
    patched.info("У patched‑логгера extra.app добавляется автоматически.")


def demo_disable_enable() -> None:
    section("8) disable()/enable(): отключение логов для конкретного модуля")

    # По имени модуля. Здесь это имя текущего файла (обычно "__main__" при запуске).
    module_name = __name__

    logger.info("Сейчас module_name = {}", module_name)
    logger.disable(module_name)
    logger.info("ЭТО НЕ ДОЛЖНО ВЫВЕСТИСЬ (логгер отключён для этого модуля).")
    logger.enable(module_name)
    logger.info("А теперь снова выводится (enable).")


def run() -> None:
    configure_console()
    configure_files()

    section("LOGURU GUIDE: зачем, как и почему — практическая демонстрация")
    logger.info("Loguru полезен, когда хочется быстрый старт, красивый вывод и мощные sink'и без боли конфигов.")
    logger.info("Ниже идут короткие разделы-демо. Параллельно создаются файлы в папке logs/.")

    demo_basics()
    demo_custom_level()
    demo_formatting_and_lazy()
    demo_bind_and_context()
    demo_filtering()
    demo_exceptions()
    demo_patch()
    demo_disable_enable()

    section("Готово")
    logger.info("Проверьте папку logs/: там есть .log, .jsonl и архивы после ротации.")


if __name__ == "__main__":
    run()


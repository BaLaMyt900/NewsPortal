from logging import LogRecord, Filter


class LevelDebug(Filter):
    """ Фильтр пропускающий только DEBUG логи """
    def filter(self, record: LogRecord) -> bool:
        return record.levelno == 10


class LevelInfo(Filter):
    """ Фильтр пропускающий только INFO логи """
    def filter(self, record: LogRecord) -> bool:
        return record.levelno == 20


class LevelWarning(Filter):
    """ Фильтр пропускающий только WARNING логи """
    def filter(self, record: LogRecord) -> bool:
        return record.levelno == 30


class LevelError(Filter):
    """ Фильтр пропускающий только ERROR логи """
    def filter(self, record: LogRecord) -> bool:
        return record.levelno == 40


class LevelCritical(Filter):
    """ Фильтр пропускающий только CRITICAL логи """
    def filter(self, record: LogRecord) -> bool:
        return record.levelno == 50

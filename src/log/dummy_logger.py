from src.log.logger import Logger


class DummyLogger(Logger):
    def info(self, message: str) -> None:
        ...

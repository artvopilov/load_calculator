from src.logger.logger import Logger


class DummyLogger(Logger):
    def info(self, message: str) -> None:
        ...

from src.log.logger import Logger


class ConsoleLogger(Logger):
    def info(self, message: str) -> None:
        print(message)

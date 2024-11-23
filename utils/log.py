import os
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from typing import Optional, Union, Literal, Dict
from threading import Lock


class Logger:
    _instance: Dict[str, 'Logger'] = {}
    _lock = Lock()

    def __init__(
            self,
            name: str,
            log_dir: str = "logs",
            log_file: str = "app.log",
            level: Union[int, str] = logging.INFO,
            rotation_type: Literal["time", "size"] = "time",
            when: str = "midnight",
            interval: int = 1,
            backup_count: int = 7,
            max_bytes: int = 1024 * 1024 * 10,  # 10MB
            encoding: str = "utf-8",
            console_output: bool = True,
            format_string: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_path = os.path.join(log_dir, log_file)

            if format_string is None:
                format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            formatter = logging.Formatter(format_string)

            if rotation_type == "time":
                file_handler = TimedRotatingFileHandler(
                    filename=log_path,
                    when=when,
                    interval=interval,
                    backupCount=backup_count,
                    encoding=encoding
                )
            else:  # size
                file_handler = RotatingFileHandler(
                    filename=log_path,
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    encoding=encoding
                )

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            if console_output:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

    @classmethod
    def get_logger(
            cls,
            name: str = "default",
            log_dir: str = "logs",
            log_file: str = "app.log",
            level: Union[int, str] = logging.INFO,
            rotation_type: Literal["time", "size"] = "time",
            when: str = "midnight",
            interval: int = 1,
            backup_count: int = 7,
            max_bytes: int = 1024 * 1024 * 10,
            encoding: str = "utf-8",
            console_output: bool = True,
            format_string: Optional[str] = None
    ) -> 'Logger':

        with cls._lock:
            if name not in cls._instance:
                cls._instance[name] = cls(
                    name=name,
                    log_dir=log_dir,
                    log_file=log_file,
                    level=level,
                    rotation_type=rotation_type,
                    when=when,
                    interval=interval,
                    backup_count=backup_count,
                    max_bytes=max_bytes,
                    encoding=encoding,
                    console_output=console_output,
                    format_string=format_string
                )
            return cls._instance[name]

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def exception(self, message: str):
        self.logger.exception(message)

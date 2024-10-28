from datetime import datetime
import logging
import inspect
from typing import Optional
import os

class Logger:
    def __init__(self, tenant_id: str, log_dir: Optional[str]) -> None:
        self.__logger = logging.Logger(__name__)
        self.__log_level = logging.DEBUG
        self.tenant_id = tenant_id
        self.log_dir = log_dir
        
        self.__setup_logger()
        
    def __setup_logger(self) -> None:
        """Setup the logger"""
        
        if self.__logger is not None:
            self.__logger.setLevel(self.__log_level)
            self.__logger.propagate = False
            
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.__log_level)
            console_handler.setFormatter(formatter)
            self.__logger.addHandler(console_handler)
            
            if self.log_dir is not None:
                if not os.path.exists(self.log_dir):
                    os.makedirs(self.log_dir)
                
                file_handler = logging.FileHandler(f"{self.log_dir}/{self.tenant_id}.log")
                file_handler.setLevel(self.__log_level)
                file_handler.setFormatter(formatter)
                self.__logger.addHandler(file_handler)
            
    
    def log_message(self, message, level="info") -> None:
        """
        Log a message with the caller's name.
        :param message: The message to log
        :param level: The log level (info, warning, error, debug)
        """
        caller_name = inspect.stack()[1].function
        message = f"[{caller_name}] [{self.tenant_id}] {message}"
        
        if level == "error":
            self.__logger.error(message)
        elif level == "warning":
            self.__logger.warning(message)
        elif level == "debug":
            self.__logger.debug(message)
        else:
            self.__logger.info(message)


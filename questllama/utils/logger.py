import time

import logging
import voyager.utils as U

class QuestLlamaLogger:
    def __init__(
                self, 
                name: str,
                log_path: str = "logs/prompts"):

        U.f_mkdir(log_path)
        self.logger = logging.getLogger(name)
        start_time = time.strftime("%Y%m%d_%H%M%S")
        handler = logging.FileHandler(U.f_join(log_path, f"{start_time}.log"))
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)


    def write_to_file(self, lines):
        """
        Write lines to a file. Used to debug LM Studio prompts.
        """
        for line in lines:
            self.logger.info(f"type: {line.type}\n")
            self.logger.info(f"content: {line.content}\n")

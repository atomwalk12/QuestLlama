import time
import re
import logging

from shared import file_utils as U

import questllama.core as tasks
import shared.config as C


class QuestLlamaLogger:
    # Class-level attribute to track if the logger has been initialized
    logger_initialized = False
    start_time = time.strftime("%Y%m%d_%H%M%S")  # Set the start time at the class level

    def __init__(self, name="OllamaAPI"):
        """
        Initializes necessary components for logging and file handling, ensuring only one log file is created.

        Parameters:
            name (str): The name of the logger.
        """
        self.log_path = C.PROMPTS_LOCATION
        self.max_tokens = 4096
        U.f_mkdir(self.log_path)

        self.logger = logging.getLogger(name)

        # Ensure that logger setup is done only once
        if not QuestLlamaLogger.logger_initialized:
            log_file_path = U.f_join(
                self.log_path, f"{QuestLlamaLogger.start_time}.log"
            )
            handler = logging.FileHandler(log_file_path, mode="a")  # Append mode

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

            # Mark as initialized to prevent further logger setup
            QuestLlamaLogger.logger_initialized = True

    def write_to_file(self, lines):
        """
        Write lines to a file. Used to debug LM Studio prompts.
        """
        for line in lines:
            self.log("info", line.type)
            self.log("info", line.text)

    def clean_ansi_sequences(self, message: str) -> str:
        """
        Remove ANSI escape sequences from a string to ensure it's plain text.
        """
        ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", message)

    def log(self, level, message, query_type="undefined"):
        """
        Write a message to the logger at a given level, after cleaning it of ANSI escape sequences.
        """
        assert message is not None

        cleaned_message = self.clean_ansi_sequences(message)
        cleaned_message = f"{query_type} - {cleaned_message}"
        if level == "error":
            self.logger.error(cleaned_message)
        elif level == "info":
            self.logger.info(cleaned_message)
        elif level == "warn":
            self.logger.warning(cleaned_message)
        else:
            raise Exception(f"Unknown log level {level}: {cleaned_message}")

    def log_phase(self, query_type, text, level="warn"):
        supported_tasks = [
            tasks.ACTION,
            tasks.CRITIC,
            tasks.SKILL,
            tasks.CURRICULUM,
            tasks.CURRICULUM_QA_STEP2_ANSWER_QUESTIONS,
            tasks.CURRICULUM_TASK_DECOMPOSITION,
            tasks.CURRICULUM_QA_STEP1_ASK_QUESTIONS,
        ]

        if query_type in supported_tasks:
            self.log(level=level, message=text, query_type=query_type)
        else:
            raise Exception("Unknown query type.")


import sys
import time
import re
from typing import Any, Dict, List

import logging
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from tokenizers import Tokenizer

from questllama.core.utils import file_utils as U
import shared.config as C


class QuestLlamaLogger:
    # Class-level attribute to track if the logger has been initialized
    logger_initialized = False
    start_time = time.strftime("%Y%m%d_%H%M%S")  # Set the start time at the class level

    def __init__(self, name: str):
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

    def log(self, level, message):
        """
        Write a message to the logger at a given level, after cleaning it of ANSI escape sequences.
        """
        cleaned_message = self.clean_ansi_sequences(message)
        if level == "error":
            self.logger.error(cleaned_message)
        elif level == "info":
            self.logger.info(cleaned_message)
        elif level == "warn":
            self.logger.warning(cleaned_message)
        else:
            raise Exception(f"Unknown log level {level}: {message}")


class LoggerCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming. Only works with LLMs that support streaming."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.logger = QuestLlamaLogger("OllamaAPI")
        self.tokenizer = Tokenizer.from_pretrained(C.TOKENIZER)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any,
    ) -> None:
        """Run when LLM starts running."""
        self.logger.write_to_file(messages[0])
        num_tokens = self.log_token_count(messages[0])
        assert num_tokens < C.CONTEXT_SIZE

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        sys.stdout.write(token)
        sys.stdout.flush()

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.logger.write_to_file([response.generations[0][0]])

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""

    def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
        """Run when chain errors."""

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Run when tool starts running."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        pass

    def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        """Run when tool ends running."""

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run on arbitrary text."""
        self.logger.log("info", text)
        num_tokens = self.log_token_count(text)
        assert num_tokens < C.CONTEXT_SIZE

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""

    def log_token_count(self, text):
        """Log to the Questllama log file message token count."""
        num_tokens = len(self.tokenizer.encode(text, add_special_tokens=True))

        self.logger.log(
            "warn", f"Context window OK: {num_tokens} < {C.CONTEXT_SIZE}"
        ) if num_tokens < C.CONTEXT_SIZE else self.logger.log(
            "error",
            f"Context window not OK: {num_tokens} > {C.CONTEXT_SIZE}",
        )
        return num_tokens

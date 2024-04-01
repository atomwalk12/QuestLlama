import sys
import time
import os
from typing import Any, Dict, List

import logging
from langchain_community.chat_models import ChatOpenAI
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

from questllama.core.utils import file_utils as U
import shared.config as C


class QuestLlamaLogger:
    def __init__(self, name: str):
        """
        Initializes necessary components for logging and file handling.

        Parameters:
            name (str): The name of the logger.
        """

        self.log_path = C.PROMPTS_LOCATION
        self.max_tokens = 4096

        # initialize ChatOpenAI and logger
        self.chat = ChatOpenAI()
        U.f_mkdir(self.log_path)

        self.logger = logging.getLogger(name)
        self.start_time = time.strftime("%Y%m%d_%H%M%S")
        handler = logging.FileHandler(U.f_join(self.log_path, f"{self.start_time}.log"))

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
            self.log("type", line.type)
            self.log("content", line.content)

    def log_num_tokens(self, messages):
        """
        Write error if number of tokens exceeds the max limit.
        """
        input = "\n".join([msg.content for msg in messages])

        tokens = self.chat.get_num_tokens(input)
        if tokens > self.max_tokens:
            self.log("error", f"Message token size: {tokens} > {self.max_tokens}.")
            sys.exit(1)
        else:
            self.log("info", f"Message token size: {tokens}.")

    def log(self, level, message):
        """
        Write a message to the logger at a given level.
        """
        if level == "error":
            self.logger.error(message)
        elif level == "info":
            self.logger.info(message)
        else:
            self.logger.warning(f"Unknown log level {level}: {message}")


class LoggerCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming. Only works with LLMs that support streaming."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.logger = QuestLlamaLogger("prompts")

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
        self.logger.log_num_tokens(messages[0])

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        sys.stdout.write(token)
        sys.stdout.flush()

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.logger.write_to_file([response.generations[0][0].message])

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

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""


class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

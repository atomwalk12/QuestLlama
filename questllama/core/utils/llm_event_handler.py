import sys
from typing import Any, Dict, List

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from tokenizers import Tokenizer
from questllama.core.utils.logger import QuestLlamaLogger

import shared.config as C


class LoggerCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming. Only works with LLMs that support streaming."""

    def __init__(self, query_type, type="OllamaAPI", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.logger = QuestLlamaLogger(name=type)
        self.query_type = query_type
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
        self.logger.log_phase(self.query_type, response.generations[0][0].type, "info")
        self.logger.log_phase(self.query_type, response.generations[0][0].text)

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
        self.logger.log_phase(query_type=self.query_type, text=text)
        num_tokens = self.log_token_count(text)
        assert num_tokens < C.CONTEXT_SIZE

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""

    def log_token_count(self, text):
        """Log to the Questllama log file message token count."""
        num_tokens = len(self.tokenizer.encode(text, add_special_tokens=True))

        self.logger.log(
            "info", f"Context window OK: {num_tokens} < {C.CONTEXT_SIZE}"
        ) if num_tokens < C.CONTEXT_SIZE else self.logger.log(
            "error",
            f"Context window not OK: {num_tokens} > {C.CONTEXT_SIZE}",
        )
        return num_tokens

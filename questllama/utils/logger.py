import time
import sys
import logging
from langchain_community.chat_models import ChatOpenAI
import voyager.utils as U

class QuestLlamaLogger:
    def __init__(self, name: str):
        self.log_path = "logs/prompts"
        self.max_tokens = 4096
        
        # initialize ChatOpenAI and logger
        self.chat = ChatOpenAI()
        U.f_mkdir(self.log_path)
        
        self.logger = logging.getLogger(name)
        self.start_time = time.strftime("%Y%m%d_%H%M%S")
        handler = logging.FileHandler(U.f_join(self.log_path, f"{self.start_time}.log"))
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
            self.log('error', f"Message token size: {tokens} > {self.max_tokens}.")
            sys.exit(1)
        else:
            self.log('info', f"Message token size: {tokens}.")
            
    def log(self, level, message):
        """
        Write a message to the logger at a given level.
        """
        if level == 'error':
            self.logger.error(message)
        elif level == 'info':
            self.logger.info(message)
        else:
            self.logger.warning(f"Unknown log level {level}: {message}")

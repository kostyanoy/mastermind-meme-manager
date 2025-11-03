from abc import ABC, abstractmethod

from src.wrappers.wrappers import MessageWrapper


class BaseHandler(ABC):
    @abstractmethod
    def send_message(self, message: MessageWrapper):
        pass

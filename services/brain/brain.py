from .online_engine import OnlineEngine
from .offline_engine import OfflineEngine


class Brain:

    def __init__(self, mode="online"):

        self.mode = mode

        if mode == "online":
            self.engine = OnlineEngine()
        else:
            self.engine = OfflineEngine()

    def generate_summary(self, text):

        return self.engine.generate_summary(text)

    def generate_keywords(self, text):

        return self.engine.generate_keywords(text)

    def generate_questions(self, text):

        return self.engine.generate_questions(text)
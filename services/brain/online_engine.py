import os

from dotenv import load_dotenv
from openai import OpenAI

from services.brain.prompts import TEACHER_PROMPT
from services.brain.model_manager import ModelManager
from services.brain.request_engine import RequestEngine
from services.brain.parser import SummaryParser

load_dotenv()


class OnlineEngine:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model_manager = ModelManager()

        self.request_engine = RequestEngine(
            self.client,
            self.model_manager,
        )

        self.summary_parser = SummaryParser()

    def generate_summary(self, text):

        print("🔥 OnlineEngine called!")

        system_prompt = TEACHER_PROMPT

        user_prompt = text

        answer = self.request_engine.request(
            system_prompt,
            user_prompt,
        )
    
        print("✅ AI Response:")
        print(answer)

        return self.summary_parser.parse(answer)

    def generate_keywords(self, text):
        return [("Placeholder", 1)]

    def generate_questions(self, text):
        return ["Placeholder"]
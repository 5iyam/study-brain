import os

from dotenv import load_dotenv

from openai import OpenAI
from openai import RateLimitError

from services.brain.prompts import TEACHER_PROMPT
from services.brain.model_manager import ModelManager

load_dotenv()


class OnlineEngine:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model_manager = ModelManager()

    def _ask_ai(self, messages):

        while True:

            model = self.model_manager.current_model()

            print(f"🤖 Trying model: {model}")

            try:

                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0,
                    max_tokens=700,
                )

                self.model_manager.reset()

                return response

            except RateLimitError:

                print(f"❌ {model} is rate limited.")

                if self.model_manager.next_model():

                    print("🔄 Switching to next model...")

                    continue

                raise Exception(
                    "All available AI models are currently rate limited."
                )

    def generate_summary(self, text):

        print("🔥 OnlineEngine called!")

        messages = [

            {
                "role": "system",
                "content": TEACHER_PROMPT,
            },

            {
                "role": "user",
                "content": text,
            }

        ]

        response = self._ask_ai(messages)

        answer = response.choices[0].message.content

        print("✅ AI Response:")
        print(answer)

        return answer.split("\n")

    def generate_keywords(self, text):
        return [("Placeholder", 1)]

    def generate_questions(self, text):
        return ["Placeholder"]
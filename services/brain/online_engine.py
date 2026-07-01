import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OnlineEngine:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = os.getenv("AI_MODEL")

    def generate_summary(self, text):

        print("🔥 OnlineEngine called!")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Say Hello in one sentence."
                }
            ]
        )

        answer = response.choices[0].message.content

        print("✅ AI Response:")
        print(answer)

        return [answer]

    def generate_keywords(self, text):
        return [("Placeholder", 1)]

    def generate_questions(self, text):
        return ["Placeholder"]
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

    def generate(self, prompt, text):

        print("🔥 OnlineEngine called!")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            temperature=0.2,
            max_tokens=700,
        )

        answer = response.choices[0].message.content

        print("✅ AI Response:")
        print(answer)

        return answer

    def generate_summary(self, prompt, text):

        return self.generate(prompt, text).split("\n")

    def generate_keywords(self, prompt, text):

        return self.generate(prompt, text)

    def generate_questions(self, prompt, text):

        return self.generate(prompt, text)
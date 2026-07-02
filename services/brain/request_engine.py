from openai import RateLimitError


class RequestEngine:

    def __init__(self, client, model_manager):

        self.client = client
        self.model_manager = model_manager

    def request(self, system_prompt, user_prompt):

        while True:

            model = self.model_manager.current_model()

            print(f"🤖 Trying model: {model}")

            try:

                response = self.client.chat.completions.create(

                    model=model,

                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],

                    temperature=0.2,
                    max_tokens=700,
                )

                print(f"✅ Using model: {model}")

                self.model_manager.reset()

                return response.choices[0].message.content

            except RateLimitError:

                print(f"❌ {model} is rate limited.")

                if self.model_manager.next_model():

                    print("🔄 Switching to next model...")

                    continue

                self.model_manager.reset()

                raise Exception(
                    "All AI models are currently rate limited."
                )
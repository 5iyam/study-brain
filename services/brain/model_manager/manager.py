# ==========================================================
# Study Brain AI Model Manager
# ==========================================================

MODELS = [

    #"cohere/north-mini-code:free",

    "nvidia/nemotron-3-ultra-550b-a55b:free",

    "qwen/qwen3-next-80b-a3b-instruct:free",

]


class ModelManager:

    def __init__(self):

        self.models = MODELS

        self.current_index = 0

    def current_model(self):

        return self.models[self.current_index]

    def next_model(self):

        self.current_index += 1

        if self.current_index >= len(self.models):

            return False

        return True

    def reset(self):

        self.current_index = 0
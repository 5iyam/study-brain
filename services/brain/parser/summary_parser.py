import json


class SummaryParser:

    def parse(self, response):

        try:

            data = json.loads(response)

            return data

        except json.JSONDecodeError:

            raise Exception(
                "AI returned invalid JSON."
            )
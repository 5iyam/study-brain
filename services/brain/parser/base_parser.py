import json


class BaseParser:

    def parse_json(self, response):

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            raise Exception(
                "AI returned invalid JSON."
            )
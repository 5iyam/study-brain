from .base_parser import BaseParser


class SummaryParser(BaseParser):

    def parse(self, response):

        data = self.parse_json(response)

        return data
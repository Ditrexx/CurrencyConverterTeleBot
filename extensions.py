import requests
import json
from config import API_KEY, currencies


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}"')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={base_ticker}{quote_ticker}&key={API_KEY}')
        data = json.loads(r.content)['data']
        ratio = tuple(data.values())[0]

        return round(float(ratio) * float(amount), 2)

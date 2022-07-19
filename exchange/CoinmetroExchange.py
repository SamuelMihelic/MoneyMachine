from curses import start_color
from requests import get
from exchange.exchange import Exchange
from pprint import pprint
from datetime import datetime

class CoinmetroExchange(Exchange):
    
    def __init__(self) -> None:
        super().__init__(name="coinmetro", authentication_info={})

        self.api_base_url = "https://api.coinmetro.com"

    def get_exchange_rate(self, currency: str, base_currency: str) -> dict:
        currency_pair = f"{currency}{base_currency}"
        query_url = f"{self.api_base_url}/exchange/prices"
        market_data_res = get(url=query_url)
        market_data_raw = market_data_res.json()
        latest_prices = market_data_raw.get('latestPrices', [])
        for info in latest_prices:
            if info.get("pair", "") == currency_pair:
                return {
                    "price": info.get("price", 0),
                    "time": datetime.utcfromtimestamp(int(info.get("timestamp", 0)) / 1000 ).strftime('%Y-%m-%d %H:%M:%S')
                }
        return {}

    def get_historic_price_data(self, currency: str, base_currency: str, start_time: str, end_time: str) -> list:
        # beginning_timestamp = datetime.strptime(start_time, '%d/%m/%Y')
        # end_timestamp = datetime.strptime(end_time, '%d/%m/%Y')
        
        query_url = f"{self.api_base_url}/exchange/candles/{currency}{base_currency}/1800000" #/{int(datetime.timestamp(beginning_timestamp)*1000)}/{int(datetime.timestamp(end_timestamp)*1000)}"
        market_data_res = get(url=query_url)
        market_data_raw = market_data_res.json()
        
        historical_data_points = market_data_raw.get('candleHistory'), []

        for dp in historical_data_points[::10000]:
            pprint(dp)
        
from requests import get
from exchange.exchange import Exchange, get_json_response
from pprint import pprint
from datetime import datetime
import csv

class CoinmetroExchange(Exchange):
    
    def __init__(self) -> None:
        super().__init__(name="coinmetro", authentication_info={})

        self.api_base_url = "https://api.coinmetro.com"

    def get_exchange_rate(self, currency: str, base_currency: str) -> dict:
        currency_pair = f"{currency}{base_currency}"
        query_url = f"{self.api_base_url}/exchange/prices"
        
        market_data = get_json_response(query_url=query_url)
        latest_prices = market_data.get('latestPrices', [])
        for info in latest_prices:
            if info.get("pair", "") == currency_pair:
                unix_timestamp = int(info.get("timestamp", 0)) / 1000
                time_string = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                price = info.get("price", 0),
                return {
                    "price": price,
                    "time": time_string
                }

        return {}
    
    def _get_historic_price_data(self, query_url: str):
        historic_data = get_json_response(query_url=query_url)
        return historic_data.get('candleHistory', [])

    # valid resolutions (ms): 60,000; 300,000; 1,800,000; 3,600,000; ...
    # valid resolutions     :    min;   5 min; half-hour;      hour; ...
    def get_historic_price_data(self, currency: str, base_currency: str, resolution: int = 1800000, start_time: int = 0, end_time: int = 0) -> list:
        if start_time == 0 or end_time == 0:
            query_url = f"{self.api_base_url}/exchange/candles/{currency}{base_currency}/{resolution}"
        else:
            query_url = f"{self.api_base_url}/exchange/candles/{currency}{base_currency}/{resolution}/{start_time}/{end_time}"

        return self._get_historic_price_data(query_url=query_url)

    def write_out_historic_data(self, historic_data: list, filepath: str):
        with open(filepath, mode="w+") as f:
            field_names = ["timestamp", "open", "close", "high", "low"]
            csv_writer = csv.DictWriter(f, delimiter=",", fieldnames=field_names)
            csv_writer.writeheader()
            for r in historic_data:
                csv_writer.writerow({
                    "timestamp": r.get("timestamp", ""),
                    "open": r.get("o", 0),
                    "close": r.get("c", 0),
                    "high": r.get("h", 0),
                    "low": r.get("l", 0),
                })

import argparse
from exchange import CoinmetroExchange
 
parser = argparse.ArgumentParser(description = "Money Machine")
 
parser.add_argument("--cm", "--coinmetro", action="store_true")
 
args = parser.parse_args()

if args.cm:
    coinmetro_exchange = CoinmetroExchange.CoinmetroExchange()
    print("Current price of BTC:")
    print(coinmetro_exchange.get_exchange_rate(currency="BTC", base_currency="USD"))
    
    print("Every 10000th data point from historical price data of BTC/USD with data granulatrity of every 30 minutes")
    coinmetro_exchange.get_historic_price_data(currency="BTC", base_currency="USD", start_time="", end_time="")
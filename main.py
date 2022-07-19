import argparse
from exchange import CoinmetroExchange
from pprint import pprint
 
parser = argparse.ArgumentParser(description = "Money Machine")
 
parser.add_argument("--cm", "--coinmetro", action="store_true")
parser.add_argument("--er", "--exchangerate", action="store_true")
parser.add_argument("--hd", "--historicdata", action="store_true")
parser.add_argument("--save", "--savedata", action="store_true")
 
args = parser.parse_args()

if args.cm:
    coinmetro_exchange = CoinmetroExchange.CoinmetroExchange()
    if args.er:
        ex_rate = coinmetro_exchange.get_exchange_rate(currency="BTC", base_currency="USD")
        print(f"Current price of BTC: {ex_rate}")

    if args.hd:
        historic_data = coinmetro_exchange.get_historic_price_data(currency="BTC", base_currency="USD")

        if args.save:
            coinmetro_exchange.write_out_historic_data(historic_data=historic_data, filepath=f"./historic_data/BTCUSD.csv")
            print("data written successfuly to ./historic_data/BTCUSD.csv")
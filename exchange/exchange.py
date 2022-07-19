from abc import ABC, abstractmethod

class Exchange(ABC):
    name: str
    api_base_url: str

    def __init__(self, name: str, authentication_info: dict):
        self.name = name
    
    @abstractmethod
    def get_exchange_rate(self, currency: str, base_currency: str) -> dict:
        pass

    @abstractmethod
    def get_historic_price_data(self, currency: str, base_currency: str, start_time: str, end_time: str) -> list:
        pass

    # TODO - UNIMPLEMENTED
    # def trade(self):
    #     pass

    # TODO - UNIMPLEMENTED
    # def update(self):
    #     pass


# class Local(Exchange):
#     pass


# class Coinmetro(Exchange):
#     pass


# class exchange: # !!! this class unfinished SAM 7/17/22
#   def __init__( self, exchange_name, account_credentials, target_asset, benchmark_asset ):
    
#     self.name  =   exchange_name
    
#     self.asset =    target_asset
#     self.bsset = benchmark_asset
  
#   if name is 'local': # for historical training purposes
#     # read from local_file (= 'market_cap_history.txt')
#     def data_extraction( self, local_file, data_duration, resolution, end_time ):
#       # expand this function here

#       self.value_history = values
#       self._time_history =  times

#     def update( self, log_market_cap ):
#       self.log_market_cap = log_market_cap # pull next datapoint from training data
    
#     def trade( self, type, quantity )
#       self.asset_by_benchmark = self.asset_by_benchmark + type * quantity # type +1 means buy, type -1 means sell (amount is in units of asset)
#       return asset_by_benchmark > 0 & asset_by_benchmark < 1 # true if did not run out of asset or benchmark funds
    
#     def update_history( data_duration, log_market_cap_history )
#       self.log_market_cap_history = log_market_cap_history
      
      
#       # log transform the values
#       values = [ log(v) for v in zip( values )]
      
#       return values, times

#   if name is 'kucoin': # https://algotrading101.com/learn/kucoin-api-guide/
#   if name is 'coinbase':
#   if name is 'coinmetro': # https://documenter.getpostman.com/view/3653795/SVfWN6KS#intro
#     import requests as rq
#     # import urllib
#     # urllib.parse.urlencode(dictionary, doseq=True)

#     is_demo = True
#     # authenticate
#     if is_demo:
#       authentication = rq.get('https://api.coinmetro.com/open/demo/temp')
#     else:
#       url = 'https://api.coinmetro.com/jwtDevice'
#       h = { 'Content-Type': 'application/x-www-form-urlencoded', \
#             'X-OTP': '', \
#             'X-Device-Id': '963844ug98wfjqd9e8v39kq' }
      
#       data = { 'login': 'some@mail.com' \
#                'password': '1passWord' }
      
#       authentication = rq.post( url, data=data, headers=headers )#.json()
      
#     def update( self ):
#       response = rq.get('https://api.coinmetro.com/exchange/prices').json()
      
#       market_cap = response.BTC.USD * number_of_tokens # how to find number of tokens?
      
#       self.log_market_cap = log( market_cap )
#       self.time1          = time.process_time()
#       self.elapsed_time = self.time1 - self.time0
#       self.time0        = self.time1
      
#     def log_market_cap_history( data_duration, resolution, end_time )
#       # all times in miliseconds
#       # valid resolution values: [ 30000, 60000, ... ]
#       start_time = end_time - data_duration
      
#       response = rq.get('https://api.coinmetro.com/exchange/candles/BTCUSD/'+str(resolution)+'/'+str(start_time)'/'+str(end_time)
    
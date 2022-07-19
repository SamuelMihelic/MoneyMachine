import time
import requests as rq
# import urllib
# urllib.parse.urlencode(dictionary, doseq=True)

class exchange: # !!! this class unfinished SAM 7/17/22
  def __init__( self, exchange_name, account_credentials, target_asset, benchmark_asset, history_duration ):
    
    self.name  =   exchange_name
    
    self.asset =    target_asset
    self.bsset = benchmark_asset

    # read from history_duration to present time
    
    # self.historical = rq.get('https://api.coinmetro.com/exchange/candles/BTCUSD/'+str(resolution)+'/'+str(start_time)'/'+str(end_time)
    self.historical = rq.get('https://api.coinmetro.com/exchange/candles/'+self.asset+self.bsset+'/86400000').json

    # if self.name is 'local': # read historical data
      # # self.historical = rq.get('https://api.coinmetro.com/exchange/candles/BTCUSD/86400000').json
      # self.historical = rq.get('https://api.coinmetro.com/exchange/candles/'+self.asset+self.bsset+'/86400000').json
    if self.name is 'coinmetro': # https://documenter.getpostman.com/view/3653795/SVfWN6KS#intro
      is_demo = True
      # authenticate
      if is_demo:
        authentication = rq.get('https://api.coinmetro.com/open/demo/temp')
      else:
        # def log_price_history( data_duration, resolution, end_time )
        # all times in miliseconds
        # valid resolution values: [ 60000, 300000, ... ]
        start_time = end_time - data_duration
        
        url = 'https://api.coinmetro.com/jwtDevice'
        h = { 'Content-Type': 'application/x-www-form-urlencoded', \
              'X-OTP': '', \
              'X-Device-Id': '963844ug98wfjqd9e8v39kq' }
        
        data = { 'login'   : account_credentials[0], \
                 'password': account_credentials[1]  }
        
        authentication = rq.post( url, data=data, headers=headers )#.json()
      self.auth = authentication

  

  # def data_extraction( self, local_file, data_duration, resolution, end_time ):
  #   # expand this function here
  # 
  #   self.value_history = values
  #   self._time_history =  times

  def update( self ):
    if self.name is 'local': # for historical training purposes
      self.log_price = csv_read(historic_data.csv,self.time_idx) # pull the time_idx'th datapoint from training data
      self.time_idx = self.time_idx+1

    if self.name is 'coinmetro':
      response = rq.get('https://api.coinmetro.com/exchange/prices').json()
      
      price = response.BTC.USD * number_of_tokens # how to find number of tokens?
      
      self.log_price = log( price )
      self.time1          = time.process_time()
      self.elapsed_time = self.time1 - self.time0
      self.time0        = self.time1
  
  def trade( self, type, quantity ):
    if self.name is 'local':
      self.asset_by_benchmark = self.asset_by_benchmark + type * quantity # type +1 means buy, type -1 means sell (amount is in units of asset)
      is_not_saturated = self.asset_by_benchmark >= 0 \
                       & self.asset_by_benchmark <= 1 # true if did not run out of asset or benchmark funds
      if self.asset_by_benchmark < 0:
        self.asset_by_benchmark = 0
      if self.asset_by_benchmark > 1:
        self.asset_by_benchmark = 1
      return is_not_saturated
    # if self.name is 'coinmetro':
      # api for trading

  
  # def update_history( data_duration, log_price_history )
    # self.log_price_history = log_price_history
    
    
    # # log transform the values
    # values = [ log(v) for v in zip( values )]
    
    # return values, times

# if name is 'kucoin': # https://algotrading101.com/learn/kucoin-api-guide/
# if name is 'coinbase':

class data:
  def __init__( self, values, times ):
    self.values = values
    self._times =  times

  def update( self, value, time ):
    self.values.append(value)
    self._times.append( time)
  
class model:
  def __init__( self, model_order, time_constant ):
    self.tau   = time_constant
    self.order = model_order
    
  def fitting( self, data ):
    # time-weighted windowing with a half-Gaussian with standard deviation equal to the time constant
    window_weights   = [ exp(-(t-data.times(-1))**2/self.tau**2/2) for t in zip( data.times )]
    
    weighted_values  = [ v * w     for v,w in zip( data.values,window_weights )]
    
    weighted_average = weighted_values.sum / window_weights.sum
    
    # calculate second moment?
    
    if     self.order is 0: # 'zero_order'
      return weighted_average
    elseif self.order is 1: # (linear here... exponential after inverse-log transform)
    elseif self.order is 2: # add the      most dominant harmonic
    elseif self.order is 3: # add the next-most dominant harmonic
    else
      # throw error
  
class error:
  def __init__( self ):
    self.P = 0
    self.I = 0
    self.D = 0
  
  def update( self, P_error, duration ):
    self.D = (      P_error - self.P ) / duration # P_error_current - P_error_before
    self.P =        P_error
    self.I = ( self.I_error + self.P ) * duration

class PID:
  def __init__( self, PID_constants ):
    self.constants =  PID_constants
    
  def update( self, error ):
    self.response = self.P * error.P \
                  + self.I * error.I \
                  + self.D * error.D

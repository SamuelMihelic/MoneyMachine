import time
import requests as rq
# import urllib
# urllib.parse.urlencode(dictionary, doseq=True)

class exchange: 
  def __init__( self, exchange_name, account_credentials, target_asset, benchmark_asset, historical_data_file, history_duration, resolution, is_demo ):
    
    self.name       =   exchange_name # coinmetro, local
    self.asset      =    target_asset # BTC
    self.bsset      = benchmark_asset # USD
    self.resolution =      resolution # [ms] time interval between samples (8640000)
    self.duration   =        duration # [ms] time to read into the past for data for the model
    self.is_demo    =         is_demo # for practicing the api trading with the exchange
    
    if self.name is 'local':
      self.time_idx = 0
      csv.open( self.historical_data_file, -r )
    else:
      csv.open( self.historical_data_file, -w )

  def authenticate( self )
    # if self.name is 'local': no authentication
    if self.name is 'coinmetro': # https://documenter.getpostman.com/view/3653795/SVfWN6KS#intro
      is_demo = True # demo server from coinmetro to practice trades
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
  
  def update( self ):        
    if self.name is 'coinmetro': # get current exchange rate from exchange
      response = rq.get('https://api.coinmetro.com/exchange/prices').json()
      self.price  = response.price.BTC
      # self.time1  = time.process_time()
      self.time1  = response.time
    
    if self.name is 'local': # pull from historical data file.csv
      # self.data_path = historic_data.csv
      self.price, self.time1 = csv.read(self.data_path,self.time_idx ) # pull the time_idx'th datapoint from price data
      self.time_idx    += 1
    else:
      csv.write(self.data_path,self.price,self.time1,--append)
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

  
  def update_history( self )

    last_prices, last_times = csv.read( self.historical_data_file ) 
  
    if self.name is 'coinmetro':
      start_time = str(int(time.process_time()-self.duration))
      end_time   = '' # optional parameter: should go to current time?
      # self.historical = rq.get('https://api.coinmetro.com/exchange/candles/BTCUSD/'+str(resolution)+'/'+str(start_time)'/'+str(end_time)
      # round self.resolution to closest valid option
      prices, times = rq.get('https://api.coinmetro.com/exchange/candles/'+self.asset+self.bsset+'/'+self.resolution+'/'+start_time+'/'+end_time).json    
    
    if self.name is 'local':
      self.time0    = last_times(0) + self.duration # read the first entry and get the timestamp add one window for the model
      prices, times = last_prices(last_times<self.time0), last_times(last_times<self.time0) # take the data points before time0 as recent history
    
    else:
      self.time0 = times[-1] # most recent timestamp from the recent historical data from the exchange
      
      # read last time off the record
      last_price, last_time = last_prices(-1), last_times(-1) 
      
      # write any more recent data to the end of the historical csv file
      csv.write(self.historical_data_file ),prices(times>last_time),\
                                             times(times>last_time),--append)
    return prices, times

# if name is 'kucoin': # https://algotrading101.com/learn/kucoin-api-guide/
# if name is 'coinbase':

class data:
  def __init__( self, values, times ):
    # read the values from the csv file instead
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

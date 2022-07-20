import csv
import time
import requests as rq
import math as m
# import urllib
# urllib.parse.urlencode(dictionary, doseq=True)

class exchange: 
  def __init__( self, historical_data_file, account_data_file, history_duration, resolution, exchange_name, target_asset, benchmark_asset, is_demo, account_credentials ):
    
    self.name       =   exchange_name # coinmetro, local
    self.asset      =    target_asset # BTC
    self.bsset      = benchmark_asset # USD
    self.resolution =      resolution # [ms] time interval between samples (8640000)
    self.duration   = history_duration # [ms] time to read into the past for data for the model
    self.log_file   = historical_data_file # for recording spot prices and times
    self.bal_file   =    account_data_file # for recording balances of assets
    
    csv_bal = open(account_data_file,'w')
    self.bal_writer = csv.writer(csv_bal, delimiter=',') # ??use DictWriter instead?
    # open for writing and go to end of file to append
    
    if self.name is 'local':
      self.time_idx = 0
      csv_log = open(self.log_file,'r') # open for reading
    else:
      csv_log = open(self.log_file,'w') # open for writing
      self.credentials = account_credentials
      self.is_demo     =             is_demo # for practicing the api trading with the exchange
      self.log_writer = csv.writer(csv_log, delimiter=',') # open for writing and go to end of file to append
      
    self.log_reader = csv.reader(csv_log, delimiter=',')
    # for row in csv_reader:
  
  def authenticate( self ):
    # if self.name is 'local': no authentication
    if self.name is 'coinmetro': # https://documenter.getpostman.com/view/3653795/SVfWN6KS#intro
      # authenticate
      if self.is_demo:
        authentication = rq.get('https://api.coinmetro.com/open/demo/temp')
      else:        
        url = 'https://api.coinmetro.com/jwtDevice'
        headers = { 'Content-Type': 'application/x-www-form-urlencoded', \
              'X-OTP': '', \
              'X-Device-Id': '963844ug98wfjqd9e8v39kq' }
        
        data = { 'login'   : self.credentials[0], \
                 'password': self.credentials[1]  }
        
        authentication = rq.post( url, data=data, headers=headers )#.json()
      self.auth = authentication
  
  def update( self ):        
    if self.name is 'coinmetro': # get current exchange rate from exchange
      response = rq.get('https://api.coinmetro.com/exchange/prices').json()
      self.price  = response.price.BTC
      # self.time1  = time.process_time()
      self.time1  = response.time
    
    if self.name is 'local': # pull from historical data file.csv
      # self.log_file = historic_data.csv
      self.time_idx    += 1
      self.price, self.time1 = self.log_reader[self.time_idx] # pull the time_idx'th datapoint from price data
      
    else:
      pause(self.resolution) # pause for time equal to the data resolution
      self.log_writer((self.price,self.time1))
      
    self.elapsed_time = self.time1 - self.time0
    self.time0        = self.time1

    return self.price, self.time
    
  def trade( self, type, quantity ):
    if self.name is 'local':
      bsset_balance0 = self.bsset_balance 
      self.bsset_balance -= type * quantity / self.price # type +1 means buy, type -1 means sell (amount is in units of asset)
      is_not_saturated = self.bsset_by_benchmark >= 0 \
                       & self.bsset_by_benchmark <= 1 # true if did not run out of asset or benchmark funds
      if self.bsset_balance < 0:
        self.bsset_balance = 0
      if self.bsset_balance > 1:
        self.bsset_balance = 1
      bsset_spent = bsset_balance0 - self.bsset_balance
      self.asset_balance += bsset_spent * self.price

      return self.asset_balance, self.bsset_balance, is_not_saturated

    if self.name is 'coinmetro':
      pass # !!!!! api for trading

  def update_history( self ):
    last_prices, last_times = csv.read( self.log_file ) 
  
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
      
      self.csv_reader.write(self.log_file,prices(times>last_time),\
                                           times(times>last_time))
    return prices, times
# if name is 'kucoin': # https://algotrading101.com/learn/kucoin-api-guide/
# if name is 'coinbase':
class data:
  def __init__( self, values, times ):
    # read the values from the csv file instead
    self.values = m.log( values ) # log transform the measurements (fold-change viewpoint)
    self._times =         times
    # !!!! MCap of the Asset (e.g. BTC) against the benchmark (e.g. USD) may be better choice than price

  def update( self, value, time ):
    
    # one datapoint in, one out !! make sure that they have the same sampling resolution !!!
    self.values(0).pop
    self._times(0).pop

    # ??? is it more efficient to pop the last data point and append to the start ???    
    self.values.append(m.log(value))
    self._times.append(       time )
  
class model:
  def __init__( self, model_order, time_constant ):
    self.tau   = time_constant
    self.order = model_order
    
  def fitting( self, data ):
    # time-weighted windowing with a half-Gaussian with standard deviation equal to the time constant
    window_weights   = [ m.exp(-(t-data._times(-1))**2/self.tau**2/2) for t in zip( data._times )]
    
    weighted_values  = [ v * w     for v,w in zip( data.values,window_weights )]
    
    weighted_average = weighted_values.sum / window_weights.sum
    
    # calculate second moment?
    
    if     self.order is 0: # 'zero_order'
      return weighted_average
    if self.order is 1:
      pass# (linear here... exponential after inverse-log transform)
    if self.order is 2:
      pass# add the      most dominant harmonic
    if self.order is 3: 
      pass# add the next-most dominant harmonic
    #else:
    #  pass# throw error
class error:
  def __init__( self ):
    self.P = 0
    self.I = 0
    self.D = 0
  
  def update( self, P_error, duration ):
    self.D = (      P_error - self.P ) / duration # P_error_current - P_error_before
    self.P =        P_error
    self.I = ( self.I       + self.P ) * duration

class PID:
  def __init__( self, PID_constants ):
    self.constants =  PID_constants
    
  def update( self, error ):
    self.response = self.P * error.P \
                  + self.I * error.I \
                  + self.D * error.D
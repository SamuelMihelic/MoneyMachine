import csv
import time
# import requests as rq
import math as m
# import urllib
# urllib.parse.urlencode(dictionary, doseq=True)

class exchange: 
  def __init__( self, history_duration, resolution, exchange_name, historical_data_file, account_data_file, target_asset, benchmark_asset, is_demo, account_credentials ):
    
    self.name       =   exchange_name # coinmetro, local
    self.asset      =    target_asset # BTC
    self.bsset      = benchmark_asset # USD
    self.resolution =      resolution # [ms] time interval between samples (8640000)
    self.duration   = history_duration # [ms] time to read into the past for data for the model
    self.log_file   = historical_data_file # for recording spot prices and times
    self.bal_file   =    account_data_file # for recording balances of assets
    self.numTrades  =           0  # running total of trades performed
    
    csv_bal = open(account_data_file+'.csv','w')
    self.bal_writer = csv.writer(csv_bal, delimiter=',') # open for writing ?? use DictWriter instead ??
    self.bal_writer.writerow(['Balances: '+self.asset     +' ['+self.bsset+']',
                                           self.bsset,'total ['+self.bsset+']',
                        'exchange rate: ['+self.asset+     ']['+self.bsset+'] / initial',
                                                         'elapsed time [days]','year', '# trades'  ])     # !!! go to end of file to append !!! ??? self.bal_writer.line_num = -1 ???

    if self.name is 'local':
      # self.asset_balance =     baseline / self.price # asset units
      # self.bsset_balance = 1 - baseline              # bsset units
      self.asset_balance = 0 # asset units
      self.bsset_balance = 1 # bsset units 1 BTC in USD in 2012
      csv_log = open(self.log_file+'.csv','r') # open for reading
    else:
      csv_log = open(self.log_file+'.csv','w') # open for appending (writing at end)
      self.credentials = account_credentials
      self.is_demo     =             is_demo # for practicing the api trading with the exchange
      self.time0 = time.process_time()
      try:
        self.log_writer = csv.writer(csv_log, delimiter=',') 

        self.log_writer.writerow([self.asset,self.bsset,'UNIX time [ms]'])
      except:
        print('Failed to find historical data log csv file in main directory')
      
    self.log_reader = csv.reader(csv_log, delimiter=',')
    self.log_reader.__next__() # skip the first row (headers)
    # for row in csv_reader:

    if self.name is 'local':
      log_row = self.log_reader.__next__()
      self.time0 = float(log_row[0])*1000+720000*self.duration # time0 is one time window from start time of log file

    self.time00  = self.time0
    
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
      # self.time_idx    += 1
      
      # advance to the next row in the log file
      log_row = self.log_reader.__next__() # pull the time_idx'th datapoint from price data
      
      self.price = 0 # to enter the loop
      while not self.price: # continue reading until non NaN value reached
        log_row = self.log_reader.__next__()
        price = float(log_row[-1])      # Weighted_Price [bsset units]
        _time = float(log_row[ 0])*1000 # Timestamp [ms]
        if not( log_row[-1] == 'NaN' ):
          self.price = price 
          self.time1 = _time
     
    else:
      time.sleep(self.resolution*1000) # pause for a time [s] equal to the data resolution [ms]
      self.log_writer.writerow([str(self.price),
                                str(self.time1) ])
      
    self.elapsed_time = self.time1 - self.time0
    self.time0        = self.time1

    return self.price, self.time1
    
  def trade( self, type, quantity ): #  quantity in bsset units
    if self.name is 'local':
      bsset_balance0      = self.bsset_balance 
      self.bsset_balance -= type * quantity # type +1 means buy, type -1 means sell (amount is in units of bsset)
      # is_not_saturated    = self.bsset_balance >= 0 \
      #                   and self.bsset_balance <= bsset_balance0 + self.asset_balance # true if did not run out of asset or benchmark funds
      if self.bsset_balance < 0:
        self.bsset_balance = 0
      if self.bsset_balance > bsset_balance0 + self.asset_balance * self.price:
        self.bsset_balance = bsset_balance0 + self.asset_balance * self.price # units of bsset
      bsset_spent         = bsset_balance0 - self.bsset_balance
      self.asset_balance += bsset_spent / self.price # units of asset
      if self.asset_balance < 0: self.asset_balance = 0

      if not( self.bsset_balance == bsset_balance0 ): self.numTrades += 1

      newRow_numbers = [ self.asset_balance * self.price,                          # bsset units
                         self.bsset_balance,                      
                         self.asset_balance * self.price + self.bsset_balance,  # exchange rate asset bsset
                                              self.price / self.price00, 
                                           (  self.time1
                                            - self.time00 ) / 1000 / 60 / 60 / 24, self.time1 / 1000 / 60 / 60 / 24 / 365 +1970, self.numTrades ] # unit of days
    
      newRow = ["{:.2f}".format(newRow_numbers[0]),
                "{:.2f}".format(newRow_numbers[1]),
                "{:.2f}".format(newRow_numbers[2]),
                "{:.2f}".format(newRow_numbers[3]),
                "{:.0f}".format(newRow_numbers[4]),
                "{:.0f}".format(newRow_numbers[5]),
                "{:.0e}".format(newRow_numbers[6]) ] # print("Geeks : %2d, Portal : %5.2f" % (1, 05.333))

      self.bal_writer.writerow(newRow)
      
      return newRow

    if self.name is 'coinmetro':
      pass # response = api for trading
      # self.asset_balance = response.assett

  def update_history( self ):
    _time = -m.inf
    # !!!!!! start at top of file (just below headers)
    # self.log_reader.line_num = 0 or self.log_file.seek(0,0)
    # self.log_reader.__next__()
    while _time < self.time0 - self.duration: # read past rows before the current time window 
      log_row = self.log_reader.__next__()
      if not( log_row[0] == 'UNIX TIME'): # !!! make sure this string encodes a number and not a header (break headers created whenever starting a new session to write to the log)
        _time = float(log_row[ 0])*1000 # Timestamp [ms] # !!!! mke fxn don't copypasta

    self.price00  = float(log_row[-1])

    _times = []
    prices = []
    while _time < self.time0: # read from start of time window up to current time
      log_row = self.log_reader.__next__()
      price = float(log_row[-1])      # Weighted_Price [bsset units]
      _time = float(log_row[ 0])*1000 # Timestamp [ms]
      if not( log_row[-1] == 'NaN' ):
        prices.append( price ) 
        _times.append( _time )
      # duration = _times[-1] \
      #          - _times[ 0] # total time of history read in and recorded
    
    if self.name is 'coinmetro':
      # self.time0 = time.process_time() # get current time 
      start_time = str(int(self.time0-self.duration))
      end_time   = '' # optional parameter: should go to current time?
      # self.historical = rq.get('https://api.coinmetro.com/exchange/candles/BTCUSD/'+str(resolution)+'/'+str(start_time)'/'+str(end_time)
      # round self.resolution to closest valid option
      self.prices, self._times = rq.get('https://api.coinmetro.com/exchange/candles/'+self.asset+self.bsset+'/'+self.resolution+'/'+start_time+'/'+end_time).json    
    
    if self.name is 'local':
      # self.time0    = _times[0] + self.duration # read the first entry and get the timestamp add one window for the model
      self.prices, self._times = prices, _times
    
    else:
      # self.time0 = self._times[-1] # most recent timestamp from the recent historical data from the exchange
      
      ## read last time off the record
      # last_price, last__time = last_prices[-1], last__times[-1] 
      # last__time = self.log_reader.last ### !!!! get the last time stamp from the csv file
      
      # write any more recent data to the end of the historical csv file
      self.log_writer.writerows(self.log_file,self.prices(self._times>_time),\
                                              self._times(self._times>_time))

    self.time0 = self._times[-1] # most recent timestamp from the recent historical data  
    
    return self.prices, self._times
# if name is 'kucoin': # https://algotrading101.com/learn/kucoin-api-guide/
# if name is 'coinbase':
# if name is 'robbhinhood': !!!!!! fewer transaction fees ?????
class data:
  def __init__( self, values, times ):
    # ??? read the values from a csv file instead ???
    self.values = [ m.log( v ) for v in values ] # log transform the measurements (fold-change viewpoint)
    self._times =                        times
    # ??? MCap of the Asset (e.g. BTC) against the benchmark (e.g. USD) may be better choice than price ???
    self.duration = times[-1] \
                  - times[ 0]
  def update( self, value, time ):
    
    # ??? is it more efficient to pop the last data point and append to the start ???    
    self.values.append(m.log(value))
    self._times.append(       time )
  
    while self._times[-1] \
        - self._times[ 1] > self.duration: # compare final time to the second to most initial time
      self.values.pop(0)
      self._times.pop(0)

class model:
  def __init__( self, model_order, time_constant ):
    self.tau   = time_constant
    self.order = model_order
    
  def fitting( self, data ):
    # time-weighted windowing with a half-Gaussian with standard deviation equal to the time constant
    window_weights   = [ m.exp(-(t-data._times[-1])**2/self.tau**2/2) for t in           data._times  ]
    weighted_values  = [           data.values[i] * window_weights[i] for i in range(len(data._times))]

    weighted_average = sum( weighted_values ) / sum( window_weights )
    
    # calculate second moment?
    
    if     self.order is 0: # 'zero_order'
      self.value = weighted_average
    if self.order is 1:
      pass# (linear here... exponential after inverse-log transform)
    if self.order is 2:
      pass# add the      most dominant harmonic
    if self.order is 3: 
      pass# add the next-most dominant harmonic
    #else:
    #  pass# throw error

    return self.value

class error:
  def __init__( self, time_constant ):
    self.P = 0
    self.I = 0
    self.D = 0

    self.time_constant = time_constant

  def update( self, P_error, elapsed_time ):
    # error time made unitless by comparing to the time constant of the model

    self.D  = ( P_error - self.P ) / elapsed_time * self.time_constant # P_error_current - P_error_before
    self.P  =   P_error
    self.I +=   P_error            * elapsed_time / self.time_constant # unitless time

class PID:
  def __init__( self, PID_constants ):
    self.P, self.I, self.D = PID_constants[0], PID_constants[1], PID_constants[2]
    
  def update( self, error ):
    self.response = self.P * error.P \
                  + self.I * error.I \
                  + self.D * error.D


    if str(self.response) == 'nan':
      self.response = 0
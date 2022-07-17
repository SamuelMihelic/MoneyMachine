class exchange: # !!! this class unfinished SAM 7/17/22
  def __init__( self, exchange_name, account_credentials, target_asset, benchmark_asset ):
    
    self.name  =   exchange_name
    
    self.asset =    target_asset
    self.bsset = benchmark_asset
  
  if name is 'local': # for historical training purposes
    def update( self, market_cap ):
      self.log_market_cap = log( market_cap ) # pull next datapoint from training data
    
    def trade( self, type, quantity )
      self.asset_by_benchmark = self.asset_by_benchmark + type * quantity # type +1 means buy, type -1 means sell (amount is in units of asset)
      return asset_by_benchmark > 0 & asset_by_benchmark < 1 # true if did not run out of asset or benchmark funds
    
    def log_market_cap_history( data_duration, resolution, end_time )
      # read from local file ('market_cap_history.txt')
      values, times = data_extraction( 'market_cap_history.txt', data_duration, resolution, end_time )
      # expand this function here
      
      # log transform the values
      values = [ log(v) for v in zip( values )]
      
      return values, times

  if name is 'kucoin':
    # https://algotrading101.com/learn/kucoin-api-guide/
    self.url   = 'www....'
    def update( self ):
      # Market cap of the target as measured against the benchmark
      # pull the current value from the exchange using API
      self.log_market_cap = kucoinAPI()
    def trade( self, type, amount )
      return is_trade_successfull

  if name is 'coinbase':
    
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

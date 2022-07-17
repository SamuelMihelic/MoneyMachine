class model:
  def __init__( self, model_order, time_constant )
    self.tau   = time_constant
    self.order = model_order
    
  def fitting( self, data )
    # time-weighted windowing with a half-Gaussian with standard deviation equal to the time constant
    window_weights       = [ exp(-(t-data.times(-1))**2/self.tau**2/2) for t in zip( data.times                 )]
    
    w_sum = window_weights.sum
    windowed_data_values = [ v * w     for v,w in zip( data.values,window_weights )]
    weighted_average     = [ w / w_sum for   w in zip(    windowed_data_values    )]
    
    # calculate second moment?
    
    if     self.order is 0 # 'zero_order'
      return weighted_average
    elseif self.order is 1 # (linear here... exponential after inverse-log transform)
    elseif self.order is 2 # add the      most dominant harmonic
    elseif self.order is 3 # add the next-most dominant harmonic
    else
      # throw error
      
class data:
  def __init__( self, values, times )
    self.values = values
    self._times =  times

  def update( self, value, time )
    self.values.append(value)
    self._times.append( time)

class PID:
  def __init__( self, PID_constants ):
    self.constants =  PID_constants
    
    self.P_error = 0
    self.I_error = 0
    self.D_error = 0
    
  def response( self, error ):
    response = self.P * error.P \
             + self.I * error.I \
             + self.D * error.D
             
    return response
  
class error:
  def __init__( self ):
    self.P = 0
    self.I = 0
    self.D = 0
  
  def update( self, P_error, duration ):
    self.D = (      P_error - self.P ) / duration # P_error_current - P_error_before
    self.P =        P_error
    self.I = ( self.I_error + self.P ) * duration

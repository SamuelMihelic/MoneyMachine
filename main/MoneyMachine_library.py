class model:
  def __init__( self, type, time_constant )
      self.tau  = time_constant
      self.type = type
    
  def fitting( self, data )
    # time-weighted windowing with a half-Gaussian
    weighted_data_values = data.values 
  
    if self.type is 'zero_order'
    elseif self.type is 'first_order'
    elseif self.type is 'second_order'
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

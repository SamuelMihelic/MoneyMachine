class PID:
  def __init__( self, PID_constants ):
    self.constants = PID_constants
    self.P_error = 0
    self.I_error = 0
    self.D_error = 0
    
  def response( self, error ):
    response = self.P * error.P \
               self.I * error.I \
               self.D * error.D
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

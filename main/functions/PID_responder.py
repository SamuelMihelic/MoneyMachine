class PID_responder:
  def __init__(self, PID_constants ):
    self.constants = PID_constants
  def update( self, error_history ):
    


def PID_responder( errors, constants, time_since_last_data )
# SAM 3/11/22
# 
# this function is the PID response portion of the PID controller.
#
# inputs are the different errors (P, I, and D), and the different constants (K_P, _I, and _D)

# we need to think about the units, so that these finite difference approximations of derivative do not depend on sampling rate
errors.D = errors.D / time_since_last_data
errors.I = errors.I * time_since_last_data

# output = errors.D * constants.D ...
       # + errors.P * constants.P ...
       # + errors.I * constants.I    
output = dot_product( errors, constants )

return output

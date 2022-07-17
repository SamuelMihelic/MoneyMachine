# MoneyMachine
            # Algorithmic crypto trading for market stability and personal profit

            # According to [the efficient market hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis) (as well as results from probability theory on [submartingales](https://en.m.wikipedia.org/wiki/Martingale_(probability_theory))), this algorithm will not outperform a simple holding strategy... But we will put this to the test, and at the very least, this algorithm will provide price stability (denoising, not trend-shifting) if enough people adopt it, through the use of [PID control](https://en.wikipedia.org/wiki/PID_controller).

## MoneyMachine Functions Overview:
            # SAM 2/19/22

import MoneyMachine_library as mm
import time

exchange1 = mm.exchange( 'kucoin', 'BTC', 'USD' )

baseline_proportion = 0.5

constants = ( 1, 1, 1 ) # PID response constants (to be learned from historical testing)
PID1 = mm.PID( constants ) # try multiple PIDs and average their outputs

error1 = mm.error() # the error history will depend on the time elapsed during the control loop
            
data1 = mm.data( values, times ) # e.g. values in $$, times in minutes

Gaussian_window_length = 60 * 24 * 7 # (one week in minutes), sliding window looking into the past from current

model1 == mm.model( 'zero_order', Gaussian_window_length )
            
time0 = time.process_time()
            
### BEGIN Section: Control Loop
#### Import Data:
            # operative quantity is market cap (MCap). not price, this is a more reliable quantity (more information)

            # https://algotrading101.com/learn/kucoin-api-guide/

            # Checking MCap hisotry
            data_duration = 6 * Gaussian_window_length # Gaussian is approx. zer0 past z-score of 5 or 6

            # MCap of the Asset (e.g. BTC) for some time into the past at a certain temporal resolution (mHz) as measured against the Benchmark asset (e.g. dollars)
            recent_price_history = Exchange_API.price( exchange_address, Asset, Benchmark_Asset, data_duration, resolution )

            # most recent price
            price = recent_price_history( end )
            
#### Data_processing:
        # log transform the measurements (fold-change viewpoint)
            price                = log( price )
            recent_price_history = log( recent_price_history )

        # Model price estimate (parameter fitting for the price model)
            # ...for the recent price history in a (Half-Gaussian) weighted window centered at current_date
            # zer0 order value (average)
            #  1st order model (exponential)
            #  2nd order model (exponential*sinusoidal)
            [ model_price, (parameter_1, parameter_2)] = model1.fitting( recemt_preice_history, model_type, Gaussian_window_length ) 

#### PID responder:
        # measure the time that has elapsed since last error measurement
        time1 = time.process_time()
        elapsed_time = time1-time0
        time0 = time1

        # difference between model and measurement (fold-difference because of log-transform)
            error1.update( price - model_price, elapsed_time )

        # PID response (inner product of errors and parameters)
            PID1.update

        # transform back to difference land (from ratio land), scaling the response to the account size, converting units
            
            response_Asset_quantity = (( exp( PID1.response ) + baseline_proportion ) * acct_value ) / exp( price )

        # difference between current and response portfolio
            trade_type     = sign( response_Asset_quantity - Asset_quantity ) # +1 means buy, -1 means sell
            trade_quantity =  abs( response_Asset_quantity - Asset_quantity )
            
#### Trading (control)
        # (Limit) Buying/Selling some amount of the target Asset (e.g. BTC) with the Benchmark asset (e.g. dollars)
            is_trade_successful  = Exchange_API.trade( exchange_address, acct_address, Asseet, Benchmark, trade_type, trade_quantity, (limit_price))

        # check acct value as measured against the Benchmark_Asset (e.g. gollars)
            acct_value           = Exchange_API.acct(  exchange_address, acct_address, Asset )

#### Feedback to account manager
            # alert user that the algo wants to buy more of the asset and running out of money, or it is losing interest in the asset
            is_email_successful = Email_Service_API( manager_address, message )
            
            # consider shorting the position if we run out of the asset

#### Chill for a second:
            chill_duration = a_second
        
            pause( chill_duration )
        
### END Section: Control Loop

### BEGIN Section: Wrappers

#### set-up (tuning):
    # (iteratively) simulate the algorithm on historic data to tune the window length, and the PID controller to maximize the profit
    [ final_acct_value_log, model_type_log, window_length_log, PID_parameters_log ] = simulate_performance( start_date, end_date, Asset, Benchmark, starting_parameters, search_method, search_parameters )
    
    # consider the tax burden (long0-term vs short-term, over or under a year)

#### execution ("here goes nothing"):
    final_acct_value = MoneyMachine( exchange_address, acct_address, manager_address, Asset, Benchmark, Gaussian_window_length, model_type, PID_parameters )

### END Section: Wrappers

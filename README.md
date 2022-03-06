# MoneyMachine
Algorithmic crypto trading for market stability and personal profit


## MoneyMachine Functions Overview:
SAM 2/19/22

### BEGIN Section: Control Loop
#### Import Data:
            # Checking price hisotry
            history_start_date = current_date - Gaussian_window_length * five_or_six # Gaussian is approx. zer0 past z-score of 5 or 6

            # price of the Asset (e.g. BTC) for some time into the past at a certain temporal resolution (mHz) as measured against the Benchmark asset (e.g. dollars)
            recent_price_history = Exchange_API.price( exchange_address, Asset, Benchmark_Asset, history_start_date, resolution )

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
            [ model_price, (parameter_1, parameter_2)] = price_model_fitting( model_type, Gaussian_window_length ) 

#### PID responder:
        # difference between model and measurement (fold-difference because of log-transform)
            D_error = price - model_price - P_error
            P_error = price - model_price
            I_error =      I_error        + P_error

        # PID response (inner product of errors and parameters)
            PID_response = PID_responder( P_error, I_error, D_error, PID_parameters )

        # transform back to difference land (from ratio land), scaling the response to the account size, converting units
            response_Asset_quantity = ( exp( PID_response ) * acct_value ) / exp( price )

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

#### Chill for a second:
            chill_duration = a_second
        
            pause( chill_duration )
        
### END Section: Control Loop

### BEGIN Section: Wrappers

#### set-up (tuning):
    # (iteratively) simulate the algorithm on historic data to tune the window length, and the PID controller to maximize the profit
    [ final_acct_value_log, model_type_log, window_length_log, PID_parameters_log ] = simulate_performance( start_date, end_date, Asset, Benchmark, starting_parameters, search_method, search_parameters )

#### execution ("here goes nothing"):
    final_acct_value = MoneyMachine( exchange_address, acct_address, manager_address, Asset, Benchmark, Gaussian_window_length, model_type, PID_parameters )

### END Section: Wrappers

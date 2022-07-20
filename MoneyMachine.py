# MoneyMachine
            # Algorithmic crypto trading for market stability and personal profit

            # According to [the efficient market hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis) (as well as results from probability theory on [submartingales](https://en.m.wikipedia.org/wiki/Martingale_(probability_theory))), this algorithm will not outperform a simple holding strategy... But we will put this to the test, and at the very least, this algorithm will provide price stability (denoising, not trend-shifting) if enough people adopt it, through the use of [PID control](https://en.wikipedia.org/wiki/PID_controller).
            # SAM 2/19/22
import MoneyMachine_library as mm

class exe:
    def __init__( self, historical_data_file, exchange_name, account_credentials, target_asset, benchmark_asset, is_demo, baseline_proportion, PID_constants, Gaussian_window_length, model_order ):
        
        resolution = 60000 # one data point read in per minute
        history_duration = 4 * Gaussian_window_length
        
        self.exch = mm.exchange( historical_data_file, history_duration, resolution, exchange_name, account_credentials, target_asset, benchmark_asset, is_demo )

        # baseline_proportion = base # portion of total benchmark invested

        # PID response constants (to be learned from historical testing)
        self.PID = mm.PID( PID_constants ) # try multiple PIDs and average their outputs

        self.err = mm.error() # the error history will depend on the time elapsed during the control loop

        # resolution = 1e-3
        self.res = Gaussian_window_length / 10

        ## Checking price hisotry
        values, times = self.exch.update_history

        self.data = mm.data( values, times ) # e.g. values in $$->math.log($$), times in miliseconds since epoch

        self.model = mm.model( model_order, Gaussian_window_length ) # sliding window looking into the past from current

        self.base = baseline_proportion


        ### BEGIN Section: Control Loop
        while True: # infinite loop

                    #### Import Data:

                    # operative quantity is market cap (MCap). not price, this is a more reliable quantity (more information)
                    self.exch.update

                    self.data.update( price, self.exch.time0 )

                    #### Data_processing:

                    # Model price estimate (parameter fitting for the price model)
                    # ...for the recent price history in a (Half-Gaussian) weighted window centered at current_date
                    # zer0 order value (average)
                    #  1st order model (exponential)
                    #  2nd order model (exponential*sinusoidal)
                    # [ model_market_cap, (parameter_1, parameter_2)] = model1.fitting( data ) 
                    log_model_market_cap = self.model.fitting( self.data ) 

                    #### PID responder:

                    # difference between model and measurement (fold-difference because of log-transform)
                    self.err.update( log_market_cap - log_model_market_cap, self.elapsed_time )

                    # PID response (inner product of errors and parameters)
                    self.PID.update( self.err )

                    # transform back to ratio land (from difference land), scaling the response to the account size, converting to benchmark units
                    response_asset_by_benchmark = exp( self.PID.response ) * self.base * self.exch.asset_by_benchmark

                    # difference between current and response portfolio
                    trade_type     = sign( response_asset_by_benchmark - self.exch.asset_by_benchmark ) # +1 means buy, -1 means sell
                    trade_quantity =  abs( response_asset_by_benchmark - self.exch.asset_by_benchmark )

                    #### Trading (control)
                    # Buying/Selling some amount of the target Asset (e.g. BTC) with the Benchmark asset (e.g. dollars)
                    is_trade_successful = self.exch.trade( trade_type, trade_quantity )

                    # check acct value as measured against the Benchmark_Asset (e.g. dollars)
                    asset_by_benchmark = self.exch.asset_by_benchmark

                    #### Feedback to account manager !!!! move to inside self.exch
                    # alert user that the algo wants to buy more of the asset and running out of money, or it is losing interest in the asset
                    if ~is_trade_successful:
                        break
                    
                    if self.name is local:
                        pass
                    else: 
                        is_email_successful = Email_Service_API( manager_address, message )
                        # consider shorting the position if we run out of the asset

                    #### Chill for a second: !!!! move to inside self.exch
                    chill_duration = 60000 # a minute

                    pause( chill_duration )

        ### END Section: Control Loop

# MoneyMachine
            # Algorithmic crypto trading for market stability and personal profit

            # According to [the efficient market hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis) (as well as results from probability theory on [submartingales](https://en.m.wikipedia.org/wiki/Martingale_(probability_theory))), this algorithm will not outperform a simple holding strategy... But we will put this to the test, and at the very least, this algorithm will provide price stability (denoising, not trend-shifting) if enough people adopt it, through the use of [PID control](https://en.wikipedia.org/wiki/PID_controller).
            # SAM 2/19/22
import MoneyMachine_library as mm
            
class exe:
            def __init__( self, exchange, account_credentials, asset, bsset, baseline_proportion, PID_constants, Gaussian_window_length, model_order )
                        
                        # account_credentials = # data structure
                        self.exch = mm.exchange( exchange, account_credentials, asset, bsset )

                        # baseline_proportion = base # portion of total benchmark invested

                        # PID response constants (to be learned from historical testing)
                        self.PID = mm.PID( PID_constants ) # try multiple PIDs and average their outputs

                        self.err = mm.error() # the error history will depend on the time elapsed during the control loop

                        ## Checking MCap hisotry
                        ### for some time into the past at a certain temporal resolution (e.g. mHz) as measured against the Benchmark asset (e.g. dollars)
                        data_duration = 6 * Gaussian_window_length # Gaussian is approx. zer0 past z-score of 5 or 6

                        # resolution = 1e-3
                        self.res = Gaussian_window_length / 10

                        values, times = exchange1.log_market_cap_history( data_duration, resolution )

                        self.data = mm.data( values, times ) # e.g. values in $$, times in minutes

                        self.model == mm.model( model_order, Gaussian_window_length ) # sliding window looking into the past from current

                        time0 = time.process_time()
                        
                        self.base = baseline_proportion

            
                        ### BEGIN Section: Control Loop
                        while True # infinite loop

                        #### Import Data:

                                    # operative quantity is market cap (MCap). not price, this is a more reliable quantity (more information)
                                    self.exch.update

                                    # MCap of the Asset (e.g. BTC) against the benchmark (e.g. USD)
                                    # log transform the measurements (fold-change viewpoint)
                                    log_market_cap = self.exch.log_market_cap

                                    self.data.update( log_market_cap, self.exch.time0 )

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
                                    if ~is_trade_successful
                                                break
                                    # consider shorting the position if we run out of the asset
                                    is_email_successful = Email_Service_API( manager_address, message )


            #### Chill for a second: !!!! move to inside self.exch
                        chill_duration = 60000 # a minute

                        pause( chill_duration )

            ### END Section: Control Loop

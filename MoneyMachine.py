# MoneyMachine
            # Algorithmic crypto trading for market stability and personal profit

            # According to [the efficient market hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis) (as well as results from probability theory on [submartingales](https://en.m.wikipedia.org/wiki/Martingale_(probability_theory))), this algorithm will not outperform a simple holding strategy... But we will put this to the test, and at the very least, this algorithm will provide price stability (denoising, not trend-shifting) if enough people adopt it, through the use of [PID control](https://en.wikipedia.org/wiki/PID_controller).
            # SAM 2/19/22
from cmath import inf
import MoneyMachine_library as mm
import math as m

class exe:
    def __init__( self, baseline_proportion, PID_constants, Gaussian_window_length, model_order, exchange_name, historical_data_file, account_data_file, target_asset, benchmark_asset, is_demo, account_credentials ):
        
        # resolution = 1e-3
        # resolution = Gaussian_window_length / 10
        resolution = 60000 # one data point read in per minute

        history_duration = 4 * Gaussian_window_length
        
        self.exch = mm.exchange( history_duration, resolution, exchange_name, historical_data_file, account_data_file, target_asset, benchmark_asset, is_demo, account_credentials )

        # baseline_proportion = base # portion of total benchmark invested

        # PID response constants (to be learned from historical testing)
        self.PID = mm.PID( PID_constants ) # try multiple PIDs and average their outputs

        self.err = mm.error( Gaussian_window_length ) # the error history will depend on the time elapsed during the control loop... or it could be brought from time zero using more historic data

        ## Checking price hisotry
        self.exch.update_history()

        self.data  = mm.data( self.exch.prices, self.exch._times ) # e.g. values in $$->math.log($$), times in miliseconds since epoch

        self.model = mm.model( model_order, Gaussian_window_length ) # sliding window looking into the past from current

        self.base = baseline_proportion

        readout_wait_time = 1000 * 60 * 60 * 24 # one day in ms
        elapsed_time0 = -inf
        total_elapsed_time = 0

        print(['Balances: '+target_asset     +' ['+benchmark_asset+']',
                                                 benchmark_asset,'total ['+benchmark_asset+']',
                                'exchange rate: ['+target_asset+     ']['+benchmark_asset+'], / initial',
                                                               'elapsed time [days]','year'  ])

        ### BEGIN Section: Control Loop
        while True: # infinite loop

            #### Import Data:
            self.exch.update()
            #### Data_processing:
            self.data.update( self.exch.price,
                              self.exch.time1  )

            # Model price estimate (parameter fitting for the price model)
            # ...for the recent price history in a (Half-Gaussian) weighted window centered at current_date
            # zer0 order value (average)
            #  1st order model (exponential)
            #  2nd order model (exponential*sinusoidal)
            # [ model_market_cap, (parameter_1, parameter_2)] = model1.fitting( data ) 
            self.model.fitting( self.data ) 

            #### PID responder:
            # difference between model and measurement (fold-difference because of log-transform)
            self.err.update( self.data.values[-1] - self.model.value, self.exch.elapsed_time )

            # PID response (inner product of errors and parameters)
            self.PID.update( self.err )

            # adjusting the PID response by the baseline proportion and scaling to the account size
            # self._PID_asset_balance = ( self.PID.response + self.base ) * ( self.exch.asset_balance * self.exch.price + self.exch.bsset_balance ) # [bsset units]
            self._PID_asset_balance = m.exp(self.PID.response) * self.exch.asset_balance # [asset units]

            if str(self._PID_asset_balance) == 'nan':
                self._PID_asset_balance = inf

            self.trade = (   self._PID_asset_balance 
                           - self.exch.asset_balance ) * self.exch.price # [bsset units]

            # difference between current and response portfolio [bsset units]
            
            if self.trade  < 0: trade_type = -1 # sell
            if self.trade  > 0: trade_type =  1 # buy
            if self.trade == 0: trade_type =  0

            trade_quantity = abs( self.trade )
            
            #### Trading (control)
            # Buying/Selling some amount [bsset units] of the target Asset (e.g. BTC) with the Benchmark asset (e.g. dollars)
            message = self.exch.trade( trade_type, trade_quantity )

            # check acct value as measured against the Benchmark_Asset (e.g. dollars)
            total_elapsed_time += self.exch.elapsed_time

            if total_elapsed_time > elapsed_time0 + readout_wait_time:
                print(",    ".join(message))
                elapsed_time0 = total_elapsed_time
            

            #### Feedback to account manager !!!! move to inside self.exch
            # alert user that the algo wants to buy more of the asset and running out of money, or it is losing interest in the asset
            if self.exch.name is 'local':
                pass
            else: 
                if ~new_balance_file_row.is_trade_successful:
                    # consider shorting the position if we run out of the asset
                    is_email_successful = self.email.send( address, message )
                    if ~is_email_successful:
                        break
                    
        ### END Section: Control Loop

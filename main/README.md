# MoneyMachine Functions Overview:
SAM 2/19/22

This README outlines the [**active account management cycle**](#Control-Loop) as well as the wrapper scripts that execute and tune the management cycle.

## Control Loop
1. Import Data:
     Checking asset hisotry (e.g. BTC for last year at 1 sample / day)
         operative quantity is market cap. not price, this is a more reliable quantity (more information)
         [API for Kucoin Exchange](https://algotrading101.com/learn/kucoin-api-guide/)
   
2. log transform the asset history (fold-change viewpoint)
   
3. Model price estimate</li>
      Parameter fitting for the price model)    
      for the recent price history in a 
      (Half-Gaussian) weighted window centered at current_date    
         zer0 order value (average)
         1st order model (exponential)
         2nd order model (exponential*sinusoidal)
   
4. [PID_responder.py](/functions/PID_responder.py)
      PID error input(s): 
         difference between model and measurement (fold-difference because of log-transform)
      PID response 
         (inner product of errors and parameters)

5. inverse transform data</li>
      back to difference land (from ratio land), scaling the response to the account size, converting units
   
6. difference between current and response portfolio</li>

7. Trading (control)</li>
      (Limit) Buying/Selling 
         some amount of the target Asset (e.g. BTC) with the Benchmark asset (e.g. dollars)
   
8. check acct value</li>
      as measured against the Benchmark_Asset (e.g. gollars)

9. Feedback to account manager</li>
      alert user that the algo wants to buy more of the asset and running out of money, or it is losing interest in the asset
      consider shorting the position if we run out of the asset

10. Chill for a second:</li>

## Wrappers

- set-up (tuning):</li>
      (iteratively) simulate the algorithm on historic data to tune the window length, and the PID controller to maximize the profit
      consider the tax burden (long0-term vs short-term, over or under a year)

- execution ("here goes nothing"):</li>

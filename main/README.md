# MoneyMachine Functions Overview:
SAM 2/19/22

## BEGIN Section: Control Loop
```
   Import Data:
      Checking asset hisotry (e.g. BTC for last year at 1 sample / day)
         operative quantity is market cap. not price, this is a more reliable quantity (more information)
         [API for Kucoin Exchange](https://algotrading101.com/learn/kucoin-api-guide/)
   
   *log transform the asset history (fold-change viewpoint)*
   
   Model price estimate 
      Parameter fitting for the price model)    
      for the recent price history in a 
      (Half-Gaussian) weighted window centered at current_date    
         zer0 order value (average)
         1st order model (exponential)
         2nd order model (exponential*sinusoidal)
   
   PID responder:
      PID error input(s): 
         difference between model and measurement (fold-difference because of log-transform)
      PID response 
         (inner product of errors and parameters)

   inverse transform data
      back to difference land (from ratio land), scaling the response to the account size, converting units
   
   difference between current and response portfolio
   Trading (control)
      (Limit) Buying/Selling 
         some amount of the target Asset (e.g. BTC) with the Benchmark asset (e.g. dollars)
   check acct value 
      as measured against the Benchmark_Asset (e.g. gollars)

   Feedback to account manager
      alert user that the algo wants to buy more of the asset and running out of money, or it is losing interest in the asset
      consider shorting the position if we run out of the asset

   Chill for a second:
```
## END Section: Control Loop

## BEGIN Section: Wrappers
```
   set-up (tuning):
      (iteratively) simulate the algorithm on historic data to tune the window length, and the PID controller to maximize the profit
      consider the tax burden (long0-term vs short-term, over or under a year)

   execution ("here goes nothing"):
```
## END Section: Wrappers

from cmath import inf
import MoneyMachine

## CuteName:
# MM = MoneyMachine Recipe # x(fold change from Jan 2018 to Mar 2021) # Num. of Trades

# note that the holding strategy has a fold change of 3.36 over this same time period

## ------------- zero order

## ----------------baseline proportion ---- PID gain ------------ model order --
## --------------------------- PID constants ---- model time constant ----------

## HypeRider: ---------------------------------------------------- zero order
# MM = MoneyMachine.exe( 0.5, (  0, 0,  1  ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x14274 # 6e5 trades
# MM = MoneyMachine.exe( 0.5, (  0, 0,  1  ), inf, 1000 * 60 * 60    , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x204
MM = MoneyMachine.exe( 0.5, (  0, 0,  1  ), inf, 1000 * 60 * 60 * 24, 1000 * 60 * 60 * 18, 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x128
# MM = MoneyMachine.exe( 0.5, (  1, 0,  1  ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1693
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e3 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x14329
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e2 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x13565
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e4 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x14246
# MM = MoneyMachine.exe( 0.5, ( 0, 0, 1e4 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x8310, 8e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, 0, 1e5 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x 12116, 6e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, 0, 1e6 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x13771, 6e5 trades
##           ---------------------------------------------------- first order
# MM = MoneyMachine.exe( 0.5, (  0, 0,  1  ), inf, 1000 * 60         , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) #  x3661 6e5 trades
# MM = MoneyMachine.exe( 0.5, (  1, 0,  0  ), inf, 1000 * 60         , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) #  x305 # 5e5 trades
# MM = MoneyMachine.exe( 0.5, (  1, 0,  0  ), inf, 1000 * 60 * 60    , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x0  ?
# MM = MoneyMachine.exe( 0.5, (  -1, 0,  0  ), inf, 1000 * 60 * 60 * 24, 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password'))

## SmartHodler: ---------------------------------------------- zero order
# MM = MoneyMachine.exe( 0.5, ( 1e3, -1, 0 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x781
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e3 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1904
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e5 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x13002
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e3 ), inf, 1000 * 60 * 60    , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x179
# MM = MoneyMachine.exe( 0.5, ( 0, -2, 1e4 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x7589, 7e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -2, 1e3 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x125, 7e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e4 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x8152, 8e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e5 ),   1, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x12021, 6e5 trades
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e3 ), inf, 1000 * 60         , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x3674 6e5 trades

# Hodler: -------------------------------------------------- zero order
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 0 ), inf, 1000 * 60           , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1.2 2e1 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 0 ),   1, 1000 * 60           , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x2.9 # 8e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -5, 0 ),   1, 1000 * 60           , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1.7 # 7e4 trades, saturation
# MM = MoneyMachine.exe( 0.5, ( 0, -2, 0 ),   1, 1000 * 60           , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x2.7 # 7e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -2, 0 ),   1, 1000 * 60 * 60      , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x2 # 2e5 trades, saturation
#        -------------------------------------------------- first order
# MM = MoneyMachine.exe( 0.5, ( 0, -2, 0 ),   1, 1000 * 60           , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password'))  # 3.0, 8e5 trades
# MM = MoneyMachine.exe( 0.5, ( 0, -2, 0 ),   1, 1000 * 60 * 60      , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # 2.5, 8e5
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 0 ), inf, 1000 * 60           , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # 1.2, 1e1
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 0 ), inf, 1000 * 60 * 60           , 1, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1, 1 trade ?

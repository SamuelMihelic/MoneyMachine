from cmath import inf
import MoneyMachine

## CuteName:
# MM = MoneyMachine Recipe #x(fold change from Jan 2018 to Mar 2021)

# note that the holding strategy has a fold change of 3.36 over this same time period

## HypeRider:
MM = MoneyMachine.exe( 0.5, ( 0, 0, 1 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x14274 # 6e5 trades total
# MM = MoneyMachine.exe( 0.5, ( 0, 0, 1 ), inf, 1000 * 60 * 60    , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x204
# MM = MoneyMachine.exe( 0.5, ( 0, 0, 1 ), inf, 1000 * 60 * 60 * 2, 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x128
# MM = MoneyMachine.exe( 0.5, ( 1, 0, 1 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1693
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e3 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x14329
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e2 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x13565
# MM = MoneyMachine.exe( 0.5, ( -1, 0, 1e4 ), inf, 1000 * 60         , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x14246


## SmartHodler:
# MM = MoneyMachine.exe( 0.5, ( 1e3, -1, 0 ), inf, 1000 * 60     , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x781
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e3 ), inf, 1000 * 60     , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x1904
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e5 ), inf, 1000 * 60     , 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x13002
# MM = MoneyMachine.exe( 0.5, ( 0, -1, 1e3 ), inf, 1000 * 60 * 60, 0, 'local', 'log', 'bal','BTC', 'USD', True, ('Username','Password')) # x179


            ### BEGIN Section: Wrappers

            #### set-up (tuning):
                # (iteratively) simulate the algorithm on historic data to tune the window length, and the PID controller to maximize the profit
                [ final_acct_value_log, model_type_log, window_length_log, PID_parameters_log ] = simulate_performance( start_date, end_date, Asset, Benchmark, starting_parameters, search_method, search_parameters )

                # consider the tax burden (long0-term vs short-term, over or under a year)

            #### execution ("here goes nothing"):
                final_acct_value = MoneyMachine( exchange_address, acct_address, manager_address, Asset, Benchmark, Gaussian_window_length, model_type, PID_parameters )

            ### END Section: Wrappers

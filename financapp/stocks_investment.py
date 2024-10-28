from utils import compound_stocks, compound_stocks_daily
from variables import my_stocks_list_data

# Example function to call compound_stocks
def main():
    # {'wallet_value': {'wallet_invested_value': 30, 
    #                   'transactions_value': 2.2, 
    #                   'wallet_real_value_now_without_transactions': 30.44157663773906, 
    #                   'wallet_real_value_now_with_transactions': 28.241576637739062, 
    #                   'wallet_per_change_no_transactions': 1.0147192212579688, 
    #                   'wallet_per_change_with_transactions': 1.0147192212579688}, 
    #                   'stocks_list': {
    #                         'AAPL': [
    #                             {'stock_symbol': 'AAPL', 
    #                             'stock_currency': 'US Dollars', 
    #                             'stock_invested_value': 10, 
    #                             'stocks_owned': 0.0443066022827338, 
    #                             'stocks_real_value': 10.362875638568838, 
    #                             'stock_change_value': 1.0362875638568838, 
    #                             'stock_change_percentage': 0.03628756385688381}], 
    #                        'ORCL': [
    #                            {'stock_symbol': 'ORCL', 
    #                             'stock_currency': 'US Dollars', 
    #                             'stock_invested_value': 10, 
    #                             'stocks_owned': 0.05914184938302912, 
    #                             'stocks_real_value': 10.22533004907882, 
    #                             'stock_change_value': 1.022533004907882, 
    #                             'stock_change_percentage': 0.022533004907882015}], 
    #                         'COST': [
    #                             {'stock_symbol': 'COST', 
    #                              'stock_currency': 'US Dollars', 
    #                              'stock_invested_value': 10, 
    #                              'stocks_owned': 0.011024750713388983, 
    #                              'stocks_real_value': 9.853370950091403, 
    #                              'stock_change_value': 0.9853370950091402, 
    #                              'stock_change_percentage': -0.01466290499085976}]}, 
    #                              'stocks_watchlist': {}} 
    # wallet_data = compound_stocks(my_stocks_list_data)
    # {'compound_stocks_daily': [{'date': datetime.date(2024, 10, 2), 'wallet_value': np.float64(1521.2158203124998)}, 
    #                            {'date': datetime.date(2024, 10, 3), 'wallet_value': np.float64(1513.505831631747)}, 
    #                            {'date': datetime.date(2024, 10, 4), 'wallet_value': np.float64(1549.787902832031)}, 
    #                            {'date': datetime.date(2024, 10, 5), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 6), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 7), 'wallet_value': np.float64(1541.7151711203833)}, 
    #                            {'date': datetime.date(2024, 10, 8), 'wallet_value': np.float64(1581.6253662109373)}, 
    #                            {'date': datetime.date(2024, 10, 9), 'wallet_value': np.float64(1617.1818126331675)}, 
    #                            {'date': datetime.date(2024, 10, 10), 'wallet_value': np.float64(9718.545532226562)}, 
    #                            {'date': datetime.date(2024, 10, 11), 'wallet_value': np.float64(9680.00030517578)}, 
    #                            {'date': datetime.date(2024, 10, 12), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 13), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 14), 'wallet_value': np.float64(9689.818226207386)}, 
    #                            {'date': datetime.date(2024, 10, 15), 'wallet_value': np.float64(9715.454378995028)}, 
    #                            {'date': datetime.date(2024, 10, 16), 'wallet_value': np.float64(9655.90917413885)}, 
    #                            {'date': datetime.date(2024, 10, 17), 'wallet_value': np.float64(9645.18155184659)}, 
    #                            {'date': datetime.date(2024, 10, 18), 'wallet_value': np.float64(9675.0)}, 
    #                            {'date': datetime.date(2024, 10, 19), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 20), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 21), 'wallet_value': np.float64(9641.181945800781)}, 
    #                            {'date': datetime.date(2024, 10, 22), 'wallet_value': np.float64(9716.363525390625)}, 
    #                            {'date': datetime.date(2024, 10, 23), 'wallet_value': np.float64(9747.908991033379)}, 
    #                            {'date': datetime.date(2024, 10, 24), 'wallet_value': np.float64(9707.272616299715)}, 
    #                            {'date': datetime.date(2024, 10, 25), 'wallet_value': np.float64(9679.454317959871)}, 
    #                            {'date': datetime.date(2024, 10, 26), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 27), 'wallet_value': 0}, 
    #                            {'date': datetime.date(2024, 10, 28), 'wallet_value': np.float64(9690.90978449041)}]}
    wallet_data = {
        "compound_stocks_real_time":compound_stocks(my_stocks_list_data),
        "compound_stocks_daily":compound_stocks_daily(my_stocks_list_data),
    }
    # wallet_data = {
    #    "compound_stocks_real_time":compound_stocks(my_stocks_list_data) 
    # }
    print(wallet_data)

# Run the main function
if __name__ == "__main__":
    main()

from utils import compound_stocks
from variables import my_stocks_list_data

# Example function to call compound_stocks
def main():
    wallet_data = compound_stocks(my_stocks_list_data)
    print(wallet_data)

# Run the main function
if __name__ == "__main__":
    main()

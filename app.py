from os import system, name
from forex_python.converter import CurrencyCodes
import src.AutoWise as AutoWise


def main():
    clear()
    print("============== Welcome to AutoWise ==============\n\n")

    auto_wise = AutoWise()

    source_currency, target_currency = prompt_currencies()
    try:

        auto_wise.set_currencies(source_currency, target_currency)

        auto_wise.set_profile_id()

        clear()
        auto_wise.setup()

        clear()
        auto_wise.start()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        input("\n\nPress enter to finish.")


def prompt_currencies():
    is_source_currency_valid = False
    is_target_currency_valid = False
    
    while not is_source_currency_valid or not is_target_currency_valid:
        # Get source currency
        if not is_source_currency_valid:
            source_currency = input(
                f"Source currency code (FROM)? (e.g. CAD) ").upper()
            
            if check_currency_code(source_currency):
                is_source_currency_valid = True

        # Get target currency
        if not is_target_currency_valid and is_source_currency_valid:
            target_currency = input(
                f"Target currency code (TO)? (e.g. USD) ").upper()

            if check_currency_code(target_currency):
                is_target_currency_valid = True


        if not is_source_currency_valid or not is_target_currency_valid:
            print("Invalid currency code\n")
        elif source_currency == target_currency:
            print("Source and target currency cannot be the same\n")


    return source_currency, target_currency


def check_currency_code(currency_code):
    c = CurrencyCodes()

    if c.get_currency_name(currency_code) is None:
        return False
    
    return True


# Clear the terminal
def clear():
    # If windows
    if name == "nt":
        system('cls')
    # If mac
    else:
        system('clear')


if __name__ == '__main__':
    main()